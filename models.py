import json
import pymysql.connections
from google.cloud.sql.connector import Connector
from sqlalchemy import Column, String, Integer, Boolean, Float, Text, ForeignKey, DateTime, TIMESTAMP, UniqueConstraint, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from math import fsum

Model = declarative_base(name='Model')
Session = None


# region Text Mined Assertion Models
class Assertion(Model):
    __tablename__ = 'assertion'
    assertion_id = Column(String(65), primary_key=True)
    subject_curie = Column(String(100))
    object_curie = Column(String(100))
    association_curie = Column(String(100))
    evidence_list = relationship('Evidence', back_populates='assertion', lazy='joined')

    def __init__(self, assertion_id, subject_curie, object_curie, association):
        self.assertion_id = assertion_id
        self.subject_curie = subject_curie
        self.object_curie = object_curie
        self.association_curie = association

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_sa_instance_state']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def get_aggregate_score(self, predicate) -> float:
        relevant_scores = [evidence.get_score() for evidence in self.evidence_list if evidence.get_top_predicate() == predicate]
        return fsum(relevant_scores) / float(len(relevant_scores))

    def get_json_attributes(self, predicate, evidence_list) -> json:
        attributes_list = [
            {
                "attribute_type_id": "biolink:original_knowledge_source",
                "value": "infores:text-mining-provider-targeted",
                "value_type_id": "biolink:InformationResource",
                "description": "The Text Mining Provider Targeted Biolink Association KP from NCATS Translator provides text-mined assertions from the biomedical literature.",
                "attribute_source": "infores:text-mining-provider-targeted"
            },
            {
                "attribute_type_id": "biolink:supporting_data_source",
                "value": "infores:pubmed",  # this will need to come from the db, eventually
                "value_type_id": "biolink:InformationResource",
                "attribute_source": "infores:text-mining-provider-targeted"
            },
            {
                "attribute_type_id": "biolink:has_evidence_count",
                "value": len(evidence_list),
                "value_type_id": "biolink:EvidenceCount",
                "description": "The count of the number of sentences that assert this edge",
                "attribute_source": "infores:text-mining-provider-targeted"
            },
            {
                "attribute_type_id": "biolink:tmkp_confidence_score",
                "value": self.get_aggregate_score(predicate),
                "value_type_id": "biolink:ConfidenceLevel",
                "description": "An aggregate confidence score that combines evidence from all sentences that support the edge",
                "attribute_source": "infores:text-mining-provider-targeted"
            },
            {
                "attribute_type_id": "biolink:supporting_document",
                "value": '|'.join([ev.document_id for ev in evidence_list]),
                "value_type_id": "biolink:Publication",
                "description": "The document(s) that contains the sentence(s) that assert the Biolink association represented by the edge; pipe-delimited",
                "attribute_source": "infores:pubmed"
            }
        ]
        for study in evidence_list:
            attributes_list.append(study.get_json_attributes())
        return json.dumps(attributes_list)


class Evidence(Model):
    __tablename__ = 'evidence'
    evidence_id = Column(String(65), primary_key=True)
    assertion_id = Column(String(65), ForeignKey('assertion.assertion_id'))
    assertion = relationship('Assertion', back_populates='evidence_list', lazy='joined')
    document_id = Column(String(45))
    sentence = Column(String(2000))
    subject_span = Column(String(45))
    subject_covered_text = Column(String(100))
    object_span = Column(String(45))
    object_covered_text = Column(String(100))
    document_zone = Column(String(45))
    document_publication_type = Column(String(100))
    document_year_published = Column(Integer)
    predicate_curie = Column(String(100))
    score = Column(Float)

    def __init__(self, evidence_id, assertion_id, document_id, sentence, subject_span, subject_covered_text,
                 object_span, object_covered_text, document_zone, document_publication_type, document_year_published,
                 predicate_curie, score):
        self.evidence_id = evidence_id
        self.assertion_id = assertion_id
        self.document_id = document_id
        self.sentence = sentence
        self.subject_span = subject_span
        self.subject_covered_text = subject_covered_text
        self.object_span = object_span
        self.object_covered_text = object_covered_text
        self.document_zone = document_zone
        self.document_publication_type = document_publication_type
        self.document_year_published = document_year_published
        self.predicate_curie = predicate_curie
        self.score = score

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_sa_instance_state']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

# endregion


def init_db(username=None, password=None):
    connector = Connector()

    def get_conn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_string="translator-text-workflow-dev:us-central1:text-mined-assertions-prod",
            driver='pymysql',
            user=username,
            password=password,
            database='targeted'
        )
        return conn

    engine = create_engine('mysql+pymysql://', creator=get_conn, echo=False)
    global Session
    Session = sessionmaker(bind=engine)
