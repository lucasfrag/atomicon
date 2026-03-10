class RuleVerdict:

    def run(self, context):

        labels = [s for _, s in context.stances]

        if "SUPPORT" in labels and "REFUTE" in labels:

            context.verdict = "CONFLICTING"

        elif "SUPPORT" in labels:

            context.verdict = "SUPPORTED"

        elif "REFUTE" in labels:

            context.verdict = "REFUTED"

        else:

            context.verdict = "NOT ENOUGH EVIDENCE"

        return context