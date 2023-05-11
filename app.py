from flask import Flask, render_template
from flask import request, jsonify
from decompose import decompose_other, decompose_implicit
from gpt import chat_gpt, chat_gpt_time
from script import ordinal_check, check_implicit, check_time_reference
from tools import get_ordinal_number, analyze_gpt
# from flask.ext.cors import CORS
import json
from suds.client import Client

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    return render_template('index.html')


@app.route('/getAnswer', methods=['GET', 'POST'])
def getAnswer():
    # url = "http://localhost:8997/myWebservice?wsdl"
    # Local Server URL
    # client = Client(url)
    question = request.args.get("question")
    # Final Pipeline
    import json
    # question = "Who is the president of US before Italy won the world cup ?"
    eflag = False
    iflag = False
    oflag = False
    keyword = None
    FINAL_ANS = None
    results = {}
    resultdic = []
    # results['subans'] = None
    eflag, keyword = check_time_reference(question)
    # print(eflag,keyword)
    if eflag is True:
        print("This is an Explicit Question!\n")
        print("Keyword: " + keyword + "\n--------------------\n")

        results['type'] = 'explicit'
        results['keyword'] = keyword

        keyword = keyword[0]
        deq = decompose_other(question, keyword)
        results['sub1'] = deq
        results['sub2'] = None
        results['subans'] = None
        resultdic = analyze_gpt(chat_gpt(deq))
        # print("The result dic is :\n" + resultdic)
        for answers in resultdic:
            # answer [1]: Start_date &  answers[2]: End_date
            if answers[1] <= keyword <= answers[2]:
                FINAL_ANS = answers[0]
                break

    iflag, keyword = check_implicit(question)

    if iflag is True and eflag is not True:
        print("This is an Implicit Question!\n")
        print("Keyword: " + keyword + "\n--------------------\n")
        results['type'] = 'implicit'
        results['keyword'] = keyword
        s1, s2 = decompose_implicit(question, keyword)
        Temporal_answer = chat_gpt_time(s2)
        results['sub1'] = s1
        results['sub2'] = s2
        results['subans'] = Temporal_answer
        print("Time for the Temporal Question: " + Temporal_answer + "\n")
        # flag, time = check_time_reference(Temporal_answer)
        # TODO: Transfer it
        # ans_sentence = chat_gpt(s1 + "in" + str(time[0]) + "?")
        resultdic = analyze_gpt(chat_gpt(s1))
        # print("The result dic is :\n" + resultdic)
        if keyword == 'before' or keyword == 'precede':
            for answers in resultdic:
                if answers[2] < Temporal_answer:
                    FINAL_ANS = answers[0]
                    break
        if keyword == 'after':
            for answers in reversed(resultdic):
                if answers[1] > Temporal_answer:
                    FINAL_ANS = answers[0]
                    break
        else:
            for answers in resultdic:
                # answer [1]: Start_date &  answers[2]: End_date
                if answers[1] <= Temporal_answer <= answers[2]:
                    FINAL_ANS = answers[0]
                    break
    oflag, keyword = ordinal_check(question)
    # print(oflag,keyword)
    if oflag is True and iflag is not True and eflag is not True:
        print("This is an Ordinal Question!\n")
        print("Keyword: " + keyword + "\n--------------------\n")
        results['type'] = 'ordinal'
        results['keyword'] = keyword
        deq = decompose_other(question, keyword)
        keyword = get_ordinal_number(keyword)
        resultdic = analyze_gpt(chat_gpt(deq))
        results['sub1'] = deq
        results['sub2'] = None
        results['subans'] = None
        # print("The result dic is :\n" + resultdic)
        if keyword == -1:  # Last
            FINAL_ANS = resultdic[0][0]
        else:
            # print(resultdic)
            # reverse_dic = resultdic.reverse()
            # resultdic[len(dict)-keyword]
            FINAL_ANS = resultdic[len(resultdic) - keyword][0]
    results['eflag'] = eflag
    results['iflag'] = iflag
    results['oflag'] = oflag
    results['FINAL_ANS'] = FINAL_ANS
    # results['keyword'] = keyword
    results['resultdic'] = [[str(x) for x in sublist] for sublist in resultdic]
    json_results = json.dumps(results)

    print("\n ---Final Answer is :", FINAL_ANS)
    print("\n\n\n\n")

    print(json_results)
    answer = json_results
    return jsonify({'answer': answer, 'keyword': results['keyword'], 'fans': FINAL_ANS, 'type': results['type'],
                    'dic': results['resultdic'], 'subq1': results['sub1'],'subq2': results['sub2'],
                    'subans': results['subans']})


@app.route('/getAnswer1', methods=['GET', 'POST'])
def getAnswer1():
    return jsonify({'answer': 1, 'keyword': 233, 'fans': 345, 'type': 'implicit',
                    'dic': [[1, 2, 2], [1, 4, 5], [8, 1, 0]], 'subq1': 'subq1',
                    'subq2':'subq2', 'subans':'subans'})


if __name__ == '__main__':
    app.run()

# eflag=eflag, oflag=oflag, iflag=iflag,
#         FINAL_ANS=FINAL_ANS, resultdic=resultdic, keyword=keyword,
#          type=result[type]
