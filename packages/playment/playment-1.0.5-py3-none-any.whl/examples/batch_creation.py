import playment

client = playment.Client("your-x-api-key-here")

try:
    batch = client.create_batch(name="test_99", label="test_99", description="label",
                                project_id="project_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
