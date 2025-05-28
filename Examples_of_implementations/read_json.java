package data_driven_examples;

import org.junit.Test;
import org.junit.Before;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
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
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Alert;
import org.openqa.selenium.Keys;
import java.util.*;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
public class read_json {
  private WebDriver driver;
  private Map<String, Object> vars;
  private JSONArray users;
  JavascriptExecutor js;
  @Before 
  public void setUp() throws IOException, ParseException {
	//System.setProperty("webdriver.chrome.driver","C:\\Users\\acer\\Downloads\\chromedriver_win32\\chromedriver.exe");
    driver = new ChromeDriver();
    js = (JavascriptExecutor) driver;
    vars = new HashMap<String, Object>();
    
    
  
	try {
		  JSONParser jsonParser = new JSONParser();
		   FileReader reader;
		reader = new FileReader("login.json");
		 //Read JSON file
		users = (JSONArray)jsonParser.parse(reader);
	

	   
	} catch (FileNotFoundException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	

   
  }
  @After
  public void tearDown() {
  //  driver.quit();
  }
  @Test
  public void sauce() throws InterruptedException { 
	  
		// Test name: sauce
	    // Step # | name | target | value
	    // 1 | open | / | 
	    driver.get("https://tutorialsninja.com/demo/");
	    // 2 | setWindowSize | 1599x961 | 
	    driver.manage().window().setSize(new Dimension(1599, 961));
	    
	    
		
	for(int i=0;i<users.size();i++) {
	JSONObject obj = (JSONObject) users.get(i);

	
    driver.findElement(By.xpath("//*[@id=\"top-links\"]/ul/li[2]/a")).click(); //dropdown
   
    driver.findElement(By.xpath("//*[@id=\"top-links\"]/ul/li[2]/ul/li[2]/a")).click(); //login
    driver.findElement(By.xpath("//*[@id=\"input-email\"]")).sendKeys((String)obj.get("username"));  // username input
    driver.findElement(By.xpath("//*[@id=\"input-password\"]")).sendKeys((String)obj.get("password")); // input password
    driver.findElement(By.xpath("//*[@id=\"content\"]/div/div[2]/div/form/input")).click(); //login click button
    
 
   if(  driver.getCurrentUrl().contains((String)obj.get("expectedResult"))){
	   System.out.println("test passed");
   }else {
	   System.out.println("test failed");
   }
   
   driver.get("http://tutorialsninja.com/demo/");
    Thread.sleep(1000);
	}
    
  
    
    

  }
}
