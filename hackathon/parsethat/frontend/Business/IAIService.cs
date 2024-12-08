using Core.Enums;

namespace Business;

public interface IAIService
{
    Task<string> ReadStructuredData(string filePath, LlmEnum llm = LlmEnum.OpenAi);
}