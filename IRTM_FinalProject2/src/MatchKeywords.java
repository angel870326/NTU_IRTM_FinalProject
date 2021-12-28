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
	private static int keywordListNum; // 公投關鍵字list數量
	private static ArrayList<String> keywordList; // 公投關鍵字
	private static ArrayList<ArrayList<String>> contentTokenList; // 議鎂做的各文章的token讀進來+docID+label預設5
//	private static ArrayList<String> matchList; // contentTokenList中包含keywordList的
//	private static ArrayList<String> unMatchList; // contentTokenList中沒有包含keywordList的

	public static void main(String[] args) throws Exception {
		/* 讀取各篇文章（各行）的token，加上docID和label預設5 */
		contentTokenList = new ArrayList<ArrayList<String>>();
		createContentTokenList();
		
		/* match keywords 並更新 label */
		keywordListNum = 4;
		for (int i = 1; i <= keywordListNum; i++) {
			// 建立公投關鍵字的 list
			keywordList = new ArrayList<String>();		
			readKeywordFile(String.format("keyword%d", i));	
			createKeywordList(keywords);
			
			// check if each element's content (String) in contentTokenList contains any keyword in keywordList
			for (int j = 0; j < contentTokenList.size(); j++) {
				int match = 0;
				for (int k = 0; k < keywordList.size(); k++) {
					if (contentTokenList.get(j).get(1).contains(keywordList.get(k))) {
						match += 1; // 計算 match 的關鍵字有幾個
					}
				}
				if (match > 1) { // match 的關鍵字大於 1 才列為相關文章
					if (contentTokenList.get(j).get(2).equals("5")) {
						contentTokenList.get(j).set(2, Integer.toString(i));
					} else {
						String label = contentTokenList.get(j).get(2);
						label = label + "," + i;
						contentTokenList.get(j).set(2, label);						
					}
				} 
			}
		}
		
		/* Write contentTokenList and unMatchList to txt file */
		writeTxt(contentTokenList, "matchKeywords");
		
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
	public static void readKeywordFile(String fileName) throws Exception {
		String pathname = String.format("src/input/%s.txt", fileName);
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
    	int count = 0;
    	ArrayList<String> firstElement = new ArrayList<String>();
    	firstElement.add(Integer.toString(count+1));
    	firstElement.add(line);
    	firstElement.add("5");
    	contentTokenList.add(firstElement);
    	count++;
    	while (line != null) {
    		line = br.readLine();
    		if (line != null) {
    	    	ArrayList<String> element = new ArrayList<String>();
    	    	element.add(Integer.toString(count+1));
    	    	element.add(line);
    	    	element.add("5");
    	    	contentTokenList.add(element);
    	    	count++;
    		} else {
    	    	br.close();
    		}
    	}
    	System.out.println("Size of contentTokenList: " + contentTokenList.size());
    	System.out.println("Check if match: " + count);
	}
	
	/**
	 * Write txt file
	 * @param txt
	 * @param fileName
	 * @throws Exception
	 */
	public static void writeTxt(ArrayList<ArrayList<String>> txt, String fileName) throws Exception {
	    File outputPath = new File(String.format("src/output/%s.txt", fileName));
	   	outputPath.createNewFile();
	   	BufferedWriter tbw_output = new BufferedWriter(new FileWriter(outputPath));
		String ouput_result = "";
	    for(int i = 0; i < txt.size(); i++) {
	   		ouput_result = ouput_result + txt.get(i).get(0).toString() + "/" + txt.get(i).get(1).toString()+ "/" + txt.get(i).get(2).toString() + "\n";
	   	}
	   	tbw_output.write(ouput_result);
	   	tbw_output.flush();
    	tbw_output.close();		
	}
}
