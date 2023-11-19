import os
import openai
from pdfminer.high_level import extract_text
from multiprocessing import Pool
from itertools import repeat

openai.api_type = "azure"
openai.api_base = ""
openai.api_version = ""
openai.api_key = ""


def pdf_to_text_conversion(pdf_path):
    text = extract_text(pdf_path)
    extracted_text = repr(text).replace("\n", " ")
    return extracted_text


def convert_qa_to_openai_format(context, question):
    prompt = """Answer the question as truthfully as possible using the provided text, and if the answer is not 
    contained within the text below, say "I don't know"

    Context:
    {0}

    Q: {1}
    A:""".format(context, question)
    return prompt


def get_response(question_set):
    response = openai.Completion.create(prompt=question_set, temperature=0, max_tokens=300, top_p=1,
                                        frequency_penalty=0, presence_penalty=0, engine="OpenAI-DaVinci-text-003")
    result = response["choices"][0]["text"].strip(" \n")
    return result


def console_ops(path, question):
    print("path is===", path)
    get_text = pdf_to_text_conversion(path)
    prompt_set = convert_qa_to_openai_format(get_text, question)
    final_res = get_response(prompt_set)
    return final_res


def final_mix_from_all_resumes(resume_folder, ask):
    pool = Pool()
    complete_res = []
    all_files = os.listdir(resume_folder)
    for file in all_files:
        resume_res = pool.starmap(console_ops, zip(repeat(resume_folder + "/" + file), ask))
        resume_res.append(file)
        complete_res.append(resume_res)
    return complete_res


# if __name__ == "__main__":
#     path_pdf = "sreejith_resume.pdf"
#     # question = "what is the last company he has worked for"
#     # question = """what is the name of candidate"""
#     text_res = console_ops(path_pdf, question)
#     print(text_res)
