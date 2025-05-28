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
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Alert;
import org.openqa.selenium.Keys;
import java.util.*;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;

import org.openqa.selenium.support.ui.Select;

public class SelectIsrael {
	
	

	private WebDriver driver;
	  private Map<String, Object> vars;
	  JavascriptExecutor js;
	  
	  @After
	  public void tearDown() {
	  //  driver.quit();
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
		  
		  
	    driver.get("http://demo.guru99.com/test/newtours/register.php");
	    driver.manage().window().setSize(new Dimension(1004, 724));
	    
	    
	    
	    
	    Select drpCountry = new Select(driver.findElement(By.name("country")));
		drpCountry.selectByVisibleText("ISRAEL");
		
		

	    
	    
	    
	    
	    
	    
	    
	    
	    
	    
	    
	 //   WebElement dropdown = driver.findElement(By.cssSelector("select[name='country']"));
	  //    dropdown.findElement(By.xpath("//option[. = 'ISRAEL']")).click();
	    
	    
	    
	  }
	
	
	  public static void main(String args[]) {
		  JUnitCore junit = new JUnitCore();
		  junit.addListener(new TextListener(System.out));
		  org.junit.runner.Result result = junit.run(SelectIsrael.class); // Replace "SampleTest" with the name of your class
		  if (result.getFailureCount() > 0) {
		    System.out.println("Test failed.");
		    System.exit(1);
		  } else {
		    System.out.println("Test finished successfully.");
		    System.exit(0);
		  }
		}
}
	