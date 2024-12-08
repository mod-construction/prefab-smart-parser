namespace infrastructure.Helpers;

public static class DirectoryHelper
{
    public static void CleanDirectory(this string directoryPath, string targetName)
    {
        foreach (var file in Directory.GetFiles(directoryPath, targetName, SearchOption.AllDirectories))
        {
            try
            {
                File.Delete(file);
            }
            catch (Exception ex)
            {
                // ignore
                Console.WriteLine($"Error deleting file {file}: {ex.Message}");
            }
        }

        var directoryName = Path.GetFileNameWithoutExtension(targetName);
        var directories = Directory.GetDirectories(directoryPath, directoryName, SearchOption.AllDirectories);
        foreach (var directory in directories)
        {
            try
            {
                Console.WriteLine($"Deleting directory: {directory}");
                Directory.Delete(directory, true);
            }
            catch (Exception ex)
            {
                // ignore
                Console.WriteLine($"Error deleting directory {directory}: {ex.Message}");
            }
        }
    }
}