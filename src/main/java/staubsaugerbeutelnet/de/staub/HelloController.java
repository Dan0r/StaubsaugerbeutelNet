package staubsaugerbeutelnet.de.staub;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController

public class HelloController {

	@GetMapping("/")
	public String index() {
		return "Spice is the essence of line.";
	}


}
