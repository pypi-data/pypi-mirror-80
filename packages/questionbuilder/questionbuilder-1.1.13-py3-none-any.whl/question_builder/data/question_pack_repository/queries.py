GET_QUESTION_PACKS = """
MATCH (questionPack:QUESTION_PACK) - [rel:HAS_QUESTION_TYPE] -> (questionType:QUESTION_TYPE)
WITH questionPack, rel.level as level, questionType order by level, rel.priority
RETURN questionPack as question_pack, level, collect(questionType) as question_types order by questionPack.code
"""
