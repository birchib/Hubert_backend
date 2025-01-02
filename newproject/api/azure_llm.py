import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

def get_llm_answer(question, documents):
    context = "\n".join([str(doc) for doc in documents])
    prompt = f"Based on the following documents:\n{context}\n\nQuestion: {question}"

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-08-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    try:
        response = client.chat.completions.create(
            model="gpt-35-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant answering questions based on provided documents."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        # Extract the content of the LLM's response
        answer = response.choices[0].message.content
        return answer  # Ensure this is a string
    except Exception as e:
        return {"error": f"Azure OpenAI API Error: {e}"}


# # Example usage
# question = "what is the appeal process for absence"
# documents = [
#      "Appeal: At any stage of the formal procedure, you have the opportunity to appeal against any disciplinary decision that has been made against you. Reasons for an appeal: • You feel the decision was unfair • You have new evidence • You disagree with the severity of the decision. Any appeal must be lodged in writing to the HR Department within five working days of the date the disciplinary/ flexible working/ absence management decision was notified to you. Your appeal should state the grounds you disagree with the disciplinary decision, including details of any new evidence.",
#      "Absence: can be split into 6 main reasons :- 1. A one off absence. Employee followed process. Includes; sick, accident, emergency, dependency etc. Priority here is to complete the return to work and support the employee if required/possible. 2. Behavioural. You identify a pattern of absence such as school run times, or Monday mornings or a team member has been Absent without leave (AWOL), Sick without following notification procedure, unauthorised absence such as leaving early to logging off without arranging time off. 3. Ongoing – you’re seeing a pattern but it’s not behavioural. Ongoing health issues, personal challenges etc. Here we need to see what support/reasonable accommodations can be given to enable them to be able to continue their role. See Employee support for ways we can support people. Scheduling, welfare meeting with HR, EAP etc. 4. Long term sick – absence was greater than 28 continuous days. 5. Maternity leave. 6. Other – Jury service. Please type in one of the 5 most common searches:- Advisor requiremenats Manger responsibilities Return to work Absence triggers Return to work meeting"
# ]

# answer = get_llm_answer(question, documents)
# print(answer)

# if __name__=="__main__":
#     main()