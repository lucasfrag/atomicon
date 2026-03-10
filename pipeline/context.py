class ClaimContext:

    def __init__(self, claim_id, claim_text, claim_date=None):
        self.id = claim_id
        self.claim = claim_text
        self.date = claim_date
        self.questions = []
        self.search_results = []
        self.documents = []
        self.stances = []
        self.passages = []
        self.evidence = []
        self.verdict = None
        self.justification = None