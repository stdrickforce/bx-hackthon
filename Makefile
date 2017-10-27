dev:
	tar -xzvf ./python/models/t1.tar.gz -C ./python/models
	tar -xzvf ./python/models/t10.tar.gz -C ./python/models

clean:
	rm -r ./python/models/t1
	rm -r ./python/models/t10
