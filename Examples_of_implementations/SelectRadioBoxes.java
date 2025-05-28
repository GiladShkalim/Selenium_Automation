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


import java.util.concurrent.TimeUnit;


public class SelectRadioBoxes {
	
	
	

	private WebDriver driver;
	  private Map<String, Object> vars;
	  JavascriptExecutor js;
	  
	  @After
	  public void tearDown() {
	 //   driver.quit();
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
		  
		  driver.get("http://demo.guru99.com/test/radio.html");	
		  
		//  driver.manage().window().setSize(new Dimension(1004, 724));
	        WebElement radio1 = driver.findElement(By.id("vfb-7-1"));							
	        WebElement radio2 = driver.findElement(By.id("vfb-7-2"));
	        
	       
	        		
	        //Radio Button1 is selected		
	        radio1.click();			
	        System.out.println("Radio Button Option 1 Selected");					
	        		
	        //Radio Button1 is de-selected and Radio Button2 is selected		
	        radio2.click();			
	        System.out.println("Radio Button Option 2 Selected");					
	        		
	        // Selecting CheckBox		
	       WebElement option1 = driver.findElement(By.id("vfb-6-1"));
	        
	        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);
	   
	        

	        
	       

	        // This will Toggle the Check box 		
	        option1.click();			

	        // Check whether the Check box is toggled on 		
	        if (option1.isSelected()) {					
	            System.out.println("Checkbox is Toggled On");					

	        } else {			
	            System.out.println("Checkbox is Toggled Off");					
	        }		
		  
		  
		  
		  
	  }
	  

	public static void main(String[] args) {
		JUnitCore junit = new JUnitCore();
		  junit.addListener(new TextListener(System.out));
		  org.junit.runner.Result result = junit.run(SelectRadioBoxes.class); // Replace "SampleTest" with the name of your class
		  if (result.getFailureCount() > 0) {
		    System.out.println("Test failed.");
		    System.exit(1);
		  } else {
		    System.out.println("Test finished successfully.");
		    System.exit(0);
		  }
		// TODO Auto-generated method stub

	}

}
