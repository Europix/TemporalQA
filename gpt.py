import openai

openai.api_key = "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"

prom = """Answer the following question with entities, numbers, or timestamps, not a text.  
Try to find all answers to this question, for instance, you should answer all entities when been asked "Who is the president of US". Multiple answers should be ranked according to their relevance to the question and separated by '||' . Here is the example question : Which Country won the World Cup?
If the time is unknown, use 0 instead for formatting and further progress. The expected answer should be formatted like this:
France (2018) || Germany (2014) || Spain (2010) || Italy (2006) || Brazil (2002) || France (1998) || Brazil (1994) || Germany (1990) || Argentina (1986) || Italy (1982) || Argentina (1978) || West Germany (1974) || Brazil (1970) || England (1966) || Brazil (1962) || Brazil (1958) || West Germany (1954) || Uruguay (1950) || Italy (1938) || Italy (1934) || Uruguay (1930)
"""


def chat_gpt(q):
    pre = "Donald Trump (2017-present) || Barack Obama (2009-2017) || George W. Bush (2001-2009) || Bill Clinton (1993-2001) || George H. W. Bush (1989-1993) || Ronald Reagan (1981-1989) || Jimmy Carter (1977-1981) || Gerald Ford (1974-1977) || Richard Nixon (1969-1974) || Lyndon B. Johnson (1963-1969) || John F. Kennedy (1961-1963) || Dwight D. Eisenhower (1953-1961) || Harry S. Truman (1945-1953) || Franklin D. Roosevelt (1933-1945) || Herbert Hoover (1929-1933) || Calvin Coolidge (1923-1929) || Warren G. Harding (1921-1923) || Woodrow Wilson (1913-1921) || William Howard Taft (1909-1913) || Theodore Roosevelt (1901-1909) || William McKinley (1897-1901) || Grover Cleveland (1893-1897) || Chester A. Arthur (1881-1885) || James A. Garfield (1881) || Rutherford B. Hayes (1877-1881) || Ulysses S. Grant (1869-1877) || Andrew Johnson (1865-1869) || Abraham Lincoln (1861-1865)"

    if "who is the president of us" in q.lower():
        return pre
    model_engine = "text-davinci-003"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prom + q,
        max_tokens=1024,
        n=10,
        stop=None,
        temperature=0.1,
        top_p=0.5
    )
    print(response.choices[0].text.strip())
    return response.choices[0].text.strip()


# chat_gpt("Why my OpenAI credit reached 18 dollars while others including one of my friends only granted 5 instead?")
# %%
def chat_gpt_time(q):
    promp = "Answer the following question with just an exact year, not a text. Try to give just a exact year instead of a time."

    model_engine = "text-davinci-003"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=promp + q,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.1,
        top_p=0.5
    )
    return response.choices[0].text.strip()
