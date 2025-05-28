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
 
public class MouseOver {
 
 private static WebDriver driver;
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
 
 public  void MO() {
 
 
 // Launch the URL 
        driver.get("https://demoqa.com/menu/");
        System.out.println("demoqa webpage Displayed");
        
    	//Maximise browser window
 driver.manage().window().fullscreen();
     
 //Adding wait 
 driver.manage().timeouts().implicitlyWait(10000, TimeUnit.MILLISECONDS);
                
        //Instantiate Action Class        
        Actions actions = new Actions(driver);
        //Retrieve WebElement 'Main Item 2' to perform mouse hover 
    	//WebElement menuOption = driver.findElement(By.xpath("//*[@id=\"nav\"]/li[2]/a"));
        
        WebElement menuOption = driver.findElement(By.linkText("Main Item 2"));
        
        
    	//Mouse hover menuOption 'Main Item 2'
    	actions.moveToElement(menuOption).perform();
    	System.out.println("Done Mouse hover on 'Main Item 2' from Menu");
    	
    	//Now Select 'Rock' from sub menu which has got displayed on mouse hover of 'Music'
    	//WebElement subMenuOption = driver.findElement(By.xpath("//*[@id=\"nav\"]/li[2]/ul/li[3]/a")); 
    	WebElement subMenuOption = driver.findElement(By.linkText("SUB SUB LIST »")); 
    	
    	
    	
    	
    	//Mouse hover menuOption 'Rock'
    	actions.moveToElement(subMenuOption).perform();
    	System.out.println("Done Mouse hover on 'Sub Item List' from Menu");
    	
    	//Now , finally, it displays the desired menu list from which required option needs to be selected
    	//Now Select 'Alternative' from sub menu which has got displayed on mouse hover of 'Rock'
    	WebElement selectMenuOption = driver.findElement(By.linkText("Sub Sub Item 1"));
    	selectMenuOption.click();
    	System.out.println("Selected 'Sub Sub Item 1' from Menu");
    	
        // Close the main window 
    	//driver.close();
 }
 
 
 public static void main(String args[]) {
	  JUnitCore junit = new JUnitCore();
	  junit.addListener(new TextListener(System.out));
	  org.junit.runner.Result result = junit.run(MouseOver.class); // Replace "SampleTest" with the name of your class
	  if (result.getFailureCount() > 0) {
	    System.out.println("Test failed.");
	    System.exit(1);
	  } else {
	    System.out.println("Test finished successfully.");
	    System.exit(0);
	  }
	}  
 
 
}












