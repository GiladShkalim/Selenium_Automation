package afeka_2024;

import org.junit.Test;
import org.junit.internal.TextListener;
import org.junit.runner.JUnitCore;
import org.junit.Before;
//import org.apache.poi.sl.usermodel.Sheet;
//import org.apache.poi.ss.usermodel.Row;
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
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.File;

import java.io.FileInputStream;

import java.io.IOException;

//import org.apache.poi.hssf.usermodel.HSSFWorkbook;

//import org.apache.poi.ss.usermodel.Row;

//import org.apache.poi.ss.usermodel.Workbook;



import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Alert;
import org.openqa.selenium.Keys;
import java.util.*;
import java.util.concurrent.TimeUnit;

import javax.naming.spi.DirStateFactory.Result;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;

public class PracticeFrames {
	

	
	private WebDriver driver;
	  private Map<String, Object> vars;
	  JavascriptExecutor js;
	  
	  
	  @After
	  public void tearDown() {
	  //  driver.quit();
	  }
	
	  
	  @Before
	  public void setUp() throws IOException {
		//System.setProperty("webdriver.chrome.driver","C:\\Users\\acer\\Downloads\\chromedriver_win32\\chromedriver.exe");
	    driver = new ChromeDriver();
	    js = (JavascriptExecutor) driver;
	    vars = new HashMap<String, Object>();
	    
	    
	
	       
	    
	  }
	  
	  
	  @Test
	  public void simple() throws InterruptedException {
		  
		
		
		   
		driver.get("https://chercher.tech/practice/frames-example-selenium-webdriver");	
		 driver.manage().window().setSize(new Dimension(1004, 724));
		
	
		 
	//	driver.findElement(By.cssSelector("body > input")).sendKeys("Hello");
		 
		 
	
		
			
			
			
			
			
			
			
			
			
			
		 
	driver.switchTo().frame("frame1");
		 
		 
	
		 
		 
		 
		 
		 
		// driver.findElement(By.cssSelector("body > input[type=text]")).sendKeys("Hello");
		driver.findElement(By.cssSelector("body > input")).sendKeys("Hello");
		

		 
		 
	
		
		
		
		
		 
		 
		 driver.switchTo().defaultContent();
		 
		 
		 driver.switchTo().frame("frame2");		   
		
		 
		 WebElement dropdown = driver.findElement(By.tagName("select"));
			//Create object for select class
			Select sel = new Select(dropdown);
			//select the 'avatar' option
			sel.selectByVisibleText("Big Baby Cat");
			
			 driver.switchTo().defaultContent();
			 
			 
			 driver.switchTo().frame("frame1");
			 
				WebElement frame3 = driver.findElement(By.xpath("//iframe[@id='frame3']"));
				// switch to frame 3
			driver.switchTo().frame(frame3);
				// find the checkbox
				
				
				//WebElement checkbox = driver.findElement(By.id("a"));
				WebElement checkbox = driver.findElement(By.xpath("//input[@type='checkbox']"));
				// if checkbox is not selected then click the checkbox
				if(! checkbox.isSelected()){
					checkbox.click();
				}
				// navigate to page level
				driver.switchTo().defaultContent();
			 
			 
			 
			 
			    
			    
		
		
			  

		  }
			
		
		  
		  
	  
	    
	  
	    
	  
	  public static void main(String args[]) {
		  JUnitCore junit = new JUnitCore();
		  junit.addListener(new TextListener(System.out));
		  org.junit.runner.Result result = junit.run(PracticeFrames.class); // Replace "SampleTest" with the name of your class
		  if (result.getFailureCount() > 0) {
		    System.out.println("Test failed.");
		    System.exit(1);
		  } else {
		    System.out.println("Test finished successfully.");
		    System.exit(0);
		  }
		}  
	  
	  
	  
	  
	  
	  
	  
	  
	  
	  
	  
	  
	  
	  

}
