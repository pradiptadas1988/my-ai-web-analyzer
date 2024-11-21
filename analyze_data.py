from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
#from langchain_openai import ChatOpenAI
#from langchain.prompts.prompt import PromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {input_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3")

#llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def analyze_dom_element(dom_chunks, input_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    # generate_prompt = PromptTemplate(
    #     input_variables=["dom_content","input_description"],
    #     template=template,
    # )
    #llm_chain = generate_prompt | llm

    generated_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        print(f"Generating batch: {i} of {len(dom_chunks)}")

        result = chain.invoke(
            {"dom_content": chunk, "input_description": input_description}
        )

        #result = llm_chain.invoke(
        #    {"dom_content": chunk, "input_description": input_description}
        #)

        generated_results.append(result)

    return "\n".join(generated_results)

    #return "\n".join(str(v) for v in generated_results)

if __name__ == "__main__":
    analyze_dom_element([], "is it empty??")