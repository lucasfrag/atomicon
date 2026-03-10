from pipeline.context import ClaimContext
from pipeline.pipeline import AveritecPipeline

from modules.llm.ollama_interface import OllamaLLM
from modules.question_generation.question_generator import QuestionGenerator
from modules.search.web_search import WebSearch
from modules.parsing.document_parser import DocumentParser
from modules.segmentation.passage_extractor import PassageExtractor
from modules.retrieval.bm25_retriever import BM25Retriever
from modules.verdict.rule_verdict import RuleVerdict
from modules.stance.llm_stance_detector import LLMStanceDetector

from modules.search.web_search import WebSearch
from dotenv import load_dotenv
import os

load_dotenv()

searcher = WebSearch(api_key=os.getenv("BRAVE_API_KEY"))

llm = OllamaLLM()
stance_detector = LLMStanceDetector(llm)
pipeline = AveritecPipeline(

    question_generator=QuestionGenerator(llm),
    searcher=searcher,
    parser=DocumentParser(),
    segmenter=PassageExtractor(),
    retriever=BM25Retriever(),
    stance_detector=stance_detector,
    verdict_predictor=RuleVerdict()
)

context = ClaimContext(
    claim_id=1,
    claim_text="Hunter Biden had no experience in the energy sector before Burisma."
)



result = pipeline.run(context)

print("\nCLAIM:")
print(result.claim)

print("\nTOP EVIDENCE:")

for evidence in result.evidence:
    print("-", evidence)

print("\nSTANCE CLASSIFICATION:")

for evidence, stance in result.stances:
    print(f"[{stance}] {evidence}")

print("\nFINAL VERDICT:")
print(result.verdict)