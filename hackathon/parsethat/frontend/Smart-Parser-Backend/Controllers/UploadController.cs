using Business;
using infrastructure.Helpers;
using Microsoft.AspNetCore.Mvc;

namespace Smart_Parser_Backend.Controllers;

[ApiController]
[Route("[controller]")]
public class UploadController : ControllerBase
{
    private readonly IAIService aiService;

    public UploadController(IAIService aiService)
    {
        this.aiService = aiService;
    }

    [HttpPost]
    public async Task<IActionResult> Post(IFormFile file)
    {
        if (file == null || file.Length == 0)
        {
            return this.BadRequest("No file uploaded.");
        }

        var uploadsFolderPath = Path.Combine(Directory.GetCurrentDirectory(), "ClientApp", "public");
        if (!Directory.Exists(uploadsFolderPath))
        {
            Directory.CreateDirectory(uploadsFolderPath);
        }

        var filePath = Path.Combine(uploadsFolderPath, file.FileName);
        await using (var stream = new FileStream(filePath, FileMode.Create))
        {
            await file.CopyToAsync(stream);
        }

        return this.Ok();
    }

    [HttpGet]
    public async Task<IActionResult> Get(string fileName)
    {
        var uploadsFolderPath = Path.Combine(Directory.GetCurrentDirectory(), "ClientApp", "public", fileName);
        var jsonData = await this.aiService.ReadStructuredData(uploadsFolderPath);
        var deletePath = Path.Combine(Directory.GetCurrentDirectory(), "ClientApp", "public");
        deletePath.CleanDirectory(fileName);
        return this.Ok(jsonData);
    }
}