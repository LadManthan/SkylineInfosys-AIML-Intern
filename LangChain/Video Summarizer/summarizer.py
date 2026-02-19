from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

class VideoSummarizer:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )
        
        self.brief_prompt = PromptTemplate.from_template(
            """
            Summarize the following transcript chunk clearly and concisely:

            {text}
            """
        )

    def generate_brief_summary(self, transcript: str):
        chunks = self.splitter.split_text(transcript)

        summaries = []
        for chunk in chunks:
            prompt = self.brief_prompt.format(text=chunk)
            response = self.llm.invoke(prompt)
            summaries.append(response.content)

        combined = "\n".join(summaries)

        final_prompt = f"Combine and refine the following summaries:\n{combined}"
        final_summary = self.llm.invoke(final_prompt)

        return final_summary.content
