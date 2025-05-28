package afeka_2024;


import org.junit.Test;
import org.junit.internal.TextListener;
import org.junit.runner.JUnitCore;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.core.IsNot.not;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import junit.framework.Assert;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Alert;
import org.openqa.selenium.Keys;
import java.util.*;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;


import org.openqa.selenium.support.ui.Select;



import java.util.Collections;
import java.io.FileReader;
import java.nio.file.Paths;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class ChangeCountry {
	
	

	private WebDriver driver;
	  private Map<String, Object> vars;
	  JavascriptExecutor js;
	  
	  @After
	  public void tearDown() {
	    driver.quit();
	  }
	
	
	  @Before
	  public void setUp() throws IOException {
	//	System.setProperty("webdriver.chrome.driver","C:\\Users\\acer\\Downloads\\chromedriver_win32\\chromedriver.exe");
	    driver = new ChromeDriver();
	    js = (JavascriptExecutor) driver;
	    vars = new HashMap<String, Object>();
	    
			    
	    
	  }
	  
	  @Test
	  public void simple() throws InterruptedException {
		  
		  
		  driver.get("https://tutorialsninja.com/demo/");
		    driver.manage().window().setSize(new Dimension(1004, 724));
	    
	    
	   

		// Find the currency dropdown button and click it
		WebElement currencyButton = driver.findElement(By.cssSelector(".btn-group > button.btn.btn-link.dropdown-toggle"));
		currencyButton.click();
		
		// Get currency options from constants.json instead of the website
		List<String> currencyOptions = new ArrayList<>();
		try {
		  String filePath = Paths.get(System.getProperty("user.dir"), 
		      "src", "test", "java", "afeka_2024", "constants.json").toString();
		  JSONParser parser = new JSONParser();
		  JSONObject jsonObject = (JSONObject) parser.parse(new FileReader(filePath));
		  JSONArray currencies = (JSONArray) jsonObject.get("currencies");
		  
		  System.out.println("Available currencies from JSON:");
		  for (Object curr : currencies) {
		    String currency = (String) curr;
		    currencyOptions.add(currency);
		    System.out.println(currency);
		  }
		} catch (Exception e) {
		  System.err.println("Error reading JSON file: " + e.getMessage());
		  e.printStackTrace();
		}
		
		// Switch to Euro
		WebElement euroOption = driver.findElement(By.name("EUR"));
		euroOption.click();
		System.out.println("Switched to Euro");
		Thread.sleep(1000);
		
		// Click currency button again
		currencyButton = driver.findElement(By.cssSelector(".btn-group > button.btn.btn-link.dropdown-toggle"));
		currencyButton.click();
		
		// Switch to Pound Sterling
		WebElement poundOption = driver.findElement(By.name("GBP"));
		poundOption.click();
		System.out.println("Switched to Pound Sterling");
		Thread.sleep(1000);
		
		// Click currency button again
		currencyButton = driver.findElement(By.cssSelector(".btn-group > button.btn.btn-link.dropdown-toggle"));
		currencyButton.click();
		
		// Switch to US Dollar
		WebElement dollarOption = driver.findElement(By.name("USD"));
		dollarOption.click();
		System.out.println("Switched to US Dollar");
		Thread.sleep(1000);
		
		// Verify the currency symbol is displayed ($ for USD)
		String pageSource = driver.getPageSource();
		assertTrue("Currency change was not successful", pageSource.contains("$"));
		System.out.println("Currency change test completed successfully");
	    
	    
	    
	  }
	
	
	  public static void main(String args[]) {
		  JUnitCore junit = new JUnitCore();
		  junit.addListener(new TextListener(System.out));
		  org.junit.runner.Result result = junit.run(ChangeCountry.class); // Replace "SampleTest" with the name of your class
		  if (result.getFailureCount() > 0) {
		    System.out.println("Test failed.");
		    System.exit(1);
		  } else {
		    System.out.println("Test finished successfully.");
		    System.exit(0);
		  }
		}
	
	
	
	
	

}
