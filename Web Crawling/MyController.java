import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

public class MyController {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		String crawlStorageFolder = "./crawl/data";
		int numberOfCrawlers = 1;
		CrawlConfig config = new CrawlConfig();
		config.setCrawlStorageFolder(crawlStorageFolder);
		int maxPagesToFetch = 10;
		int maxDepthOfCrawling = 16;
		int politenessDelay = 200;
		
		config.setMaxDepthOfCrawling(maxDepthOfCrawling);
		config.setMaxPagesToFetch(maxPagesToFetch);
		config.setPolitenessDelay(politenessDelay);
		//config.setUserAgentString(userAgentString);
		config.setIncludeBinaryContentInCrawling(true);
		
		
		
		
		
		PageFetcher pageFetcher = new PageFetcher(config);
		RobotstxtConfig txtConfig  = new RobotstxtConfig();
		RobotstxtServer txtServer = new RobotstxtServer(txtConfig, pageFetcher);
		CrawlController controller = new CrawlController(config,pageFetcher,txtServer);
		
		//resume crawler
		
		
		controller.addSeed([news_site]);
		
		controller.start(MyCrawler.class, numberOfCrawlers);

	}

}
