package staubsaugerbeutelnet.de.staub;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.stereotype.Controller;

@Controller
public class HomeController{



	@GetMapping("/")
	public String home() {
		return "index";
	}
	
	//@GetMapping("/edeka")
	//public String showProducts(Model model) {
	//	Vacuum vacuum1 = new Vacuum(productIdh "1", productBrand: "EDEKA", productName: "EO5", productVacuum: "AAM 6100");
	//}

}
