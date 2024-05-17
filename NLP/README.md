## Data description:

<p>The <em>dataset</em> folder contains the following files:</p>

<ul>
	<li><em>train.csv</em>: 90 x 2</li>
	<li><em>test.csv</em>: 60 x 1</li>
  <li><em>trainResumes</em>:  90 resumes that you must use for training model</li>
	<li><em>testResumes</em>: 60 resumes that you must use for testing model</li>
  <li><em>Job description.pdf</em>: PDF file that represents the job description of a Machine Learning engineer</li>
  
</ul>

## Evaluation metric:
score = 100*max(0, 1 - metrics.mean_squared_log_error(actual, predicted)

## Best Model:
make an google api key from here - https://aistudio.google.com/app/apikey

How to Use -
1. just run python app.py.
2. open postman.
3. Go on Body. -> select Form data.
4. make 2 keys 'resume' and 'job_description' select type of both as file.
5. make a POST request on it.
