using Core.AppSettings;
using Core.Enums;
using Microsoft.Extensions.Options;

namespace Business;

public class AIService : IAIService
{
    private readonly AiApiUrls urls;

    public AIService(IOptions<AiApiUrls> urls)
    {
        this.urls = urls.Value;
    }

    public async Task<string> ReadStructuredData(string filePath, LlmEnum llm)
    {
        if (llm != LlmEnum.OpenAi)
        {
            throw new ArgumentOutOfRangeException(nameof(llm), "selected llm is not supported");
        }

        const string parameterName = "input";
        var apiUrl = $"{this.urls.OpenAI}?{parameterName}={filePath}";
        using var client = new HttpClient();
        var response = await client.GetAsync(apiUrl);
        response.EnsureSuccessStatusCode();
        var responseData = await response.Content.ReadAsStringAsync();
        return responseData;
    }
}