from settings import OPEN_KEY
from chatgpt import openai


def generate_prompt():
    say = """Suggest three names for an animal that is a superhero.

    Animal: Cat
    Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
    Animal: Dog
    Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
    Animal: Pig
    Names:"""
    return say


def test1():
    model = "text-davinci-003"
    # model = "gpt-3.5-turbo"
    prompt = generate_prompt()
    prompt = "怎么实现一个B+树?"
    temperature = 0.6

    resp = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature
    )

    ret = resp.choices[0].text
    print(resp.choices)
    print(dir(resp))
    print(ret)



def test2():
    engines = openai.Engine.list()
    print(engines)


def test3():
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "谁是linus?"}
        ]
    )

    print(f"choices type: {type(completion.choices[0])}")
    print(completion.choices[0].message)


def main():
    # test1()
    # test2()
    test3()


if __name__ == "__main__":
    main()
