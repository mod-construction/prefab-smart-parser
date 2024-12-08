using Business;

var builder = WebApplication.CreateBuilder(args);

// Configure Kestrel server timeouts
builder.WebHost.ConfigureKestrel(
    options =>
    {
        options.Limits.RequestHeadersTimeout = TimeSpan.FromMinutes(10);
        options.Limits.KeepAliveTimeout = TimeSpan.FromMinutes(10);
        options.Limits.MaxRequestBodySize = 1000 * 1024 * 1024;
    });

builder.Services.AddScoped<IAIService, AIService>();

builder.Services.AddControllersWithViews();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment()) { }

app.UseStaticFiles();
app.UseRouting();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller}/{action=Index}/{id?}");

app.MapFallbackToFile("index.html");

app.Run();