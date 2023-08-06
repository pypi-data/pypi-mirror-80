import playment

client = playment.Client("your-x-api-key-here")

"""
Get Job Result Data
"""
try:
    job_result = client.get_job_result(project_id="project_id",
                                       job_id="job_id")
except playment.exception.PlaymentException as e:
    print(e.code, e.message, e.data)
