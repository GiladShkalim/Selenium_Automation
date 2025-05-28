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


public class Boxes {
	
	
	

	private WebDriver driver;
	  private Map<String, Object> vars;
	  JavascriptExecutor js;
	  
	  @After
	  public void tearDown() {
	 //   driver.quit();
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
		  
		  driver.get("http://the-internet.herokuapp.com/checkboxes");
		  
		
		  
		//*[@id="checkboxes"]/input[1]
		  
		//  #checkboxes > input[type=checkbox]:nth-child(1)
		  
		  
		//*[@id="checkboxes"]/input[2]

		  
		  
		  
		//*[@id="checkboxes"]/input[1]
		  
		
		  
		  
		  WebElement option1 = driver.findElement(By.xpath("//input[@type='checkbox'][1]"));
		  WebElement option2 = driver.findElement(By.xpath("//input[@type='checkbox'][2]"));
		  
		//*[@id="checkboxes"]/input[1]
		//option1.click();
		//option2.click();
		
	
		
	
		
		
		
		
		
		
		
		
		
		
		  
	
		  
		  
		 if(!option1.isSelected()) { option1.click();
		 
		 System.out.println("checked option1");
		 }
		 if(!option2.isSelected()) { option2.click();
		 System.out.println("checked option2");}
		 
		 
		 
		 
		 
		 
		 
		 
	        
		 

	        // This will Toggle the Check box 
		  
		  for(int i=0;i<2;i++) {
	        option1.click();
	       
	        for(int j=0;j<2;j++) {
	        
	        option2.click();
	      
	        // Check whether the Check box is toggled on 		
	        if (option1.isSelected()) {					
	            System.out.println("Checkbox1 is Toggled On "+i+" "+j);					

	        } else {			
	            System.out.println("Checkbox1 is Toggled Off "+i+" "+j);					
	        }
	        
	        if (option2.isSelected()) {					
	            System.out.println("Checkbox2 is Toggled On "+i+" "+j);					

	        } else {			
	            System.out.println("Checkbox2 is Toggled Off "+i+" "+j);					
	        }
	        }
		  }
		  
		  
		  
	  }
	  

	public static void main(String[] args) {
		JUnitCore junit = new JUnitCore();
		  junit.addListener(new TextListener(System.out));
		  org.junit.runner.Result result = junit.run(Boxes.class); // Replace "SampleTest" with the name of your class
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
