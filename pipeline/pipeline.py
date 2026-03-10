class AveritecPipeline:

    def __init__(self,
                 question_generator,
                 searcher,
                 parser,
                 segmenter,
                 retriever,
                 stance_detector,
                 verdict_predictor):

        self.question_generator = question_generator
        self.searcher = searcher
        self.parser = parser
        self.segmenter = segmenter
        self.retriever = retriever
        self.stance_detector = stance_detector
        self.verdict_predictor = verdict_predictor

    def run(self, context):

        context = self.question_generator.run(context)
        context = self.searcher.run(context)
        context = self.parser.run(context)
        context = self.segmenter.run(context)
        context = self.retriever.run(context)
        context = self.stance_detector.run(context)
        context = self.verdict_predictor.run(context)

        return context