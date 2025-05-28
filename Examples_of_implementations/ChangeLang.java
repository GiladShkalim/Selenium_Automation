package afeka_2024;

import org.junit.Test;
import org.junit.internal.TextListener;
import org.junit.runner.JUnitCore;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.JavascriptExecutor;
import java.util.*;
import java.io.FileReader;
import java.nio.file.Paths;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class ChangeLang {

    private WebDriver driver;
    private Map<String, Object> vars;
    JavascriptExecutor js;

    @After
    public void tearDown() {
        driver.quit();
    }

    @Before
    public void setUp() throws IOException {
        driver = new ChromeDriver();
        js = (JavascriptExecutor) driver;
        vars = new HashMap<String, Object>();
    }

    @Test
    public void changeLanguage() throws InterruptedException {
        driver.get("https://www.ticketor.com/demo/foodanddrink");
        driver.manage().window().setSize(new Dimension(1004, 724));

        // Find the language dropdown button and click it
        WebElement languageButton = driver.findElement(By.cssSelector(".language-selector"));
        languageButton.click();

        // Get language options from constants.json
        List<String> languageOptions = new ArrayList<>();
        try {
            String filePath = Paths.get(System.getProperty("user.dir"), 
                "src", "test", "java", "afeka_2024", "constants.json").toString();
            JSONParser parser = new JSONParser();
            JSONObject jsonObject = (JSONObject) parser.parse(new FileReader(filePath));
            JSONArray languages = (JSONArray) jsonObject.get("languages");

            System.out.println("Available languages from JSON:");
            for (Object lang : languages) {
                String language = (String) lang;
                languageOptions.add(language);
                System.out.println(language);
            }
        } catch (Exception e) {
            System.err.println("Error reading JSON file: " + e.getMessage());
            e.printStackTrace();
        }

        // Switch between languages
        for (String lang : languageOptions) {
            WebElement langOption = driver.findElement(By.linkText(lang));
            langOption.click();
            System.out.println("Switched to " + lang);
            Thread.sleep(1000);
            languageButton.click(); // Reopen the dropdown for the next selection
        }

        System.out.println("Language change test completed successfully");
    }

    public static void main(String args[]) {
        JUnitCore junit = new JUnitCore();
        junit.addListener(new TextListener(System.out));
        org.junit.runner.Result result = junit.run(ChangeLang.class);
        if (result.getFailureCount() > 0) {
            System.out.println("Test failed.");
            System.exit(1);
        } else {
            System.out.println("Test finished successfully.");
            System.exit(0);
        }
    }
}
