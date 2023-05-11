
def decompose_implicit(target_question, keyword):
    split_question = target_question.split(keyword)
    sub1 = split_question[0] + "?"
    sub2 = keyword + split_question[1]
    return sub1, sub2
# print (chat_gpt(decompose_implicit("who won best actor when alfred junge won best art direction", "when")))


def decompose_other(target_question, keyword):
    output = target_question.replace(str(keyword),'')
    output = output.replace("in", '')
    return output
