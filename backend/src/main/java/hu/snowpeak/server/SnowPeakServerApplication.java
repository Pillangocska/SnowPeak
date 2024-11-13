package hu.snowpeak.server;

import hu.snowpeak.server.config.rabbitmq.RabbitMQProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SnowPeakServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(SnowPeakServerApplication.class, args);
	}

	@Bean
	public CommandLineRunner runner(RabbitMQProducer rabbitMQProducer) {
		return args -> {
			// Add a small delay to ensure RabbitMQ connection is established
			Thread.sleep(5000);
			rabbitMQProducer.sendMessage("{\"status\": \"connected to RabbitMQ!\"}");
		};
	}
}
