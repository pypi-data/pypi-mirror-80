class DataQuestion:
    def __init__(
        self,
        content,
        interest,
        target_lemma,
        target_word,
        pos,
        tag=None,
        verbgames_pattern_items=None,
        bait_content=None,
    ):
        self.content = content
        self.interest = interest
        self.target_lemma = target_lemma
        self.target_word = target_word
        self.pos = pos
        self.tag = tag
        self.verbgames_pattern_items = verbgames_pattern_items
        self.bait_content = bait_content

    def __repr__(self):
        return "DataQuestion({}, {} , {} , {} , {} , {} , {} )".format(
            self.content,
            self.target_lemma,
            self.target_word,
            self.pos,
            self.tag,
            self.verbgames_pattern_items,
            self.bait_content.id if self.bait_content else None,
        )
