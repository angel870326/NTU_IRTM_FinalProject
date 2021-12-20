import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.util.ArrayList;

/**
 * 根據 keyword.txt 第一行的關鍵字找出相關的文章
 */
public class MatchKeywords {
	private static String keywords; // 公投關鍵字
	private static ArrayList<String> keywordList; // 公投關鍵字
	private static ArrayList<String> contentTokenList; //議鎂做的各文章的token讀進來
	private static ArrayList<String> matchList; // contentTokenList中包含keywordList的
	private static ArrayList<String> unMatchList; // contentTokenList中沒有包含keywordList的

	public static void main(String[] args) throws Exception {
		/* 建立公投關鍵字的 list */
		keywordList = new ArrayList<String>();
		readKeywordFile();
		createKeywordList(keywords);
		
		/* 讀取各篇文章（各行）的token */
		contentTokenList = new ArrayList<String>();
		createContentTokenList();
		
		/* check if each element (String) in contentTokenList contains any keyword in keywordList */
		matchList = new ArrayList<String>();
		unMatchList = new ArrayList<String>();
		for (int i = 0; i < contentTokenList.size(); i++) {
			int match = 0;
			for (int j = 0; j < keywordList.size(); j++) {
				if (contentTokenList.get(i).contains(keywordList.get(j))) {
					match += 1; // 計算 match 的關鍵字有幾個
				}
			}
			if (match > 1) { // match 的關鍵字大於 1 才列為相關文章
				matchList.add(contentTokenList.get(i));
			} 
			else {
				unMatchList.add(contentTokenList.get(i));
			}
		}
		System.out.println("Size of matchList: " + matchList.size());
		System.out.println("Size of unMatchList: " + unMatchList.size());
		if (contentTokenList.size() == matchList.size() + unMatchList.size()) {
			System.out.println("Matching is correct!");
		} else {
			System.out.println("Matching is wrong......");
		}
		
		/* Write matchList and unMatchList to txt file */
		writeTxt(matchList, "match_content");
//		writeTxt(unMatchList, "unMatch_content");
		
	}
	
	/**
	 * create keywordList
	 * @param k is keywords from keyword.txt
	 */
	public static void createKeywordList(String k) {		
		/* 找出 splitter 的 index */
		char split = ',';
		ArrayList<Integer> splitIndex = new ArrayList<Integer>();
		for(int i = 0; i < k.length(); i++) {
			if(k.charAt(i) == split) {
				splitIndex.add(i);
			}
		}
		/* 找出每個詞的開頭 index */
		ArrayList<Integer> starIndex = new ArrayList<Integer>();
		starIndex.add(0);
		for(int i = 0; i < splitIndex.size()-1; i++) {
			int star = splitIndex.get(i) + 1;
			starIndex.add(star);
		}
		/* 找出每個詞的結尾 index */
		ArrayList<Integer> endIndex = new ArrayList<Integer>();
		for(int i = 0; i < splitIndex.size(); i++) {
			int end = splitIndex.get(i) - 1;
			endIndex.add(end);
		}
		/* check if starIndex size = endIndex size */
//		if(starIndex.size() == endIndex.size()) {
//			System.out.println("Split:" + splitIndex);
//			System.out.println("Start:" + starIndex);
//			System.out.println("End  :" + endIndex);
//		}
		/* create keywordList */
		for (int i = 0; i < starIndex.size(); i++) {
			int star = starIndex.get(i);
			int end = endIndex.get(i);
			String str = "";
			for (int j = star; j <= end; j++) {
				str += k.charAt(j) ;
			}
			keywordList.add(str);
		}
		/* check keywordList */
		System.out.println("keywordList: " + keywordList);
	}

	/**
	 * Read keyword.txt（預設只有一行）
	 * keyword.txt 的內容最後必須以 ',' 結尾！
	 * @throws Exception
	 */
	public static void readKeywordFile() throws Exception {
		String pathname = "src/input/keyword.txt";
    	File filename = new File(pathname);
    	InputStreamReader reader = new InputStreamReader(new FileInputStream(filename));
    	BufferedReader br = new BufferedReader(reader);
    	String line = br.readLine();
    	keywords = line;
    	br.close();
	}

	/**
	 * Read content_token_ckip.txt
	 * @throws Exception
	 */
	public static void createContentTokenList() throws Exception {
    	String pathname = "src/input/content_token_ckip.txt";
    	File filename = new File(pathname);
    	InputStreamReader reader = new InputStreamReader(new FileInputStream(filename));
    	BufferedReader br = new BufferedReader(reader);
    	String line = br.readLine();
    	contentTokenList.add(line);
    	while (line != null) {
    		line = br.readLine();
    		if (line != null) {
    	    	contentTokenList.add(line);
    		} else {
    	    	br.close();
    		}
    	}
    	System.out.println("Size of contentTokenList: " + contentTokenList.size());
	}
	
	public static void writeTxt(ArrayList<String> txt, String fileName) throws Exception {
	    File outputPath = new File(String.format("src/output/%s.txt", fileName));
	   	outputPath.createNewFile();
	   	BufferedWriter tbw_output = new BufferedWriter(new FileWriter(outputPath));
		String ouput_result = "";
	    for(int i = 0; i < txt.size(); i++) {
	   		ouput_result = ouput_result + txt.get(i).toString() + "\n";
	   	}
	   	tbw_output.write(ouput_result);
	   	tbw_output.flush();
    	tbw_output.close();		
	}
}
