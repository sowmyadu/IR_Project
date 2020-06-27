import org.apache.hadoop.io.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;
import java.util.HashMap;
import java.util.StringTokenizer;

class WordCountMapper extends Mapper<LongWritable,Text, Text, Text>
{

	//private static final IntWritable = new IntWritable(1);
	private Text word = new Text();

	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException{

		String line = value.toSring();
		String document[] = line.split("\t",2);
		String content = document[1];
		// convert to lowercase , replace special characters and punctuation, numerals, \t by space;
		String lower = content.toLowerCase().replaceAll("[^a-z]"," ");
		String input = content.replaceAll("\\s+"," ");

		Text docID = new Text(document[0]);
		StringTokenizer tokens = new StringTokenizer(input);
		while(tokens.hasMoreTokens()) {
			word.set(tokens.nextToken());
			context.write(word,docID);
		}
	}

}

class WordCountReducer extends Reducer<Text, Text, Text, Text> {

	public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException{

				HashMap<String,Integer> wordCounter = new HashMap<String, Integer>();
				for(Text val: values)
        {
               String value = val.toString();
               if(wordCounter.containsKey(value))
                {
                       //temp = (IntWritable)counter.get(val);
                       int count = wordCounter.get(value);
                       count += 1;
                       wordCounter.put(value, count);
                }
               	else
               	{
                       wordCounter.put(value, 1);
                }
        }
        StringBuilder sb = new StringBuilder();
        for(String key: wordCounter.keySet())
        {
                sb.append(key+":"+wordCounter.get(key)+" ");
        }
        Text output = new Text(sb.toString());
        context.write(key, output);
				//		int sum = 0;
				//		for(IntWritable value:values) {
				//			sum+=value.get();
				//		}
				//
				//		context.write(key, new IntWritable(sum));

	}

}

public class InvertedIndexJob {
	public static void main(String args[]) throws IOException, ClassNotFoundException, InterruptedException{
		if(args.length!=2) {
			System.err.println("Error in input: Word Count <niput path> <output path>");
			System.exit(-1);
		}
		Configuration config = new Configuration();
		Job job = Job.getInstance(config,"WordCount");
		job.setJarByClass(InvertedIndexJob.class);
		//job.setJobName("WordCount");
		FileInputFormat.addInputPath(job,new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		//setting mapper and reducer class
		job.setMapperClass(WordCountMapper.class);
		job.setReducerClass(WordCountReducer.class);

		//setting output key and value
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.WaitForCompletion(true);

	}
}
