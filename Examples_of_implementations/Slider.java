package afeka_2024;







import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.internal.TextListener;
import org.junit.runner.JUnitCore;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;
 
public class Slider {
 
 private static WebDriver driver;
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
 
 public  void Sliding() {
 
 
 // Launch the URL 
        driver.get("https://demoqa.com/slider/");
        System.out.println("demoqa webpage Displayed");
        
    	//Maximise browser window
driver.manage().window().maximize();
     
 //Adding wait 
 driver.manage().timeouts().implicitlyWait(30000, TimeUnit.MILLISECONDS);
                
        //Instantiate Action Class        
       Actions actions = new Actions(driver);
     
        
        WebElement slider = driver.findElement(By.xpath("//input[@type='range']"));
        
        
        
        actions.moveToElement(slider,25,150).perform();
    	slider.click();
    	System.out.println("Moved slider in horizontal directions");
        
    	
    	
        // Close the main window 
    	//driver.close();
 }
 
 
 public static void main(String args[]) {
	  JUnitCore junit = new JUnitCore();
	  junit.addListener(new TextListener(System.out));
	  org.junit.runner.Result result = junit.run(Slider.class); // Replace "SampleTest" with the name of your class
	  if (result.getFailureCount() > 0) {
	    System.out.println("Test failed.");
	    System.exit(1);
	  } else {
	    System.out.println("Test finished successfully.");
	    System.exit(0);
	  }
	}  
 
 
}













