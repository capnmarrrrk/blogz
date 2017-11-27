package org.launchcode.cheesemvc.controllers;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpServletRequest;
import java.util.ArrayList;
import java.util.HashMap;

@Controller
//every url has to be preceded by /cheese
@RequestMapping("cheese")
public class CheeseController{
    HashMap<String, String> cheeses =  new HashMap<>();


    @RequestMapping(value = "")

    public String index(Model model) {


        model.addAttribute("cheeses", cheeses);
        model.addAttribute("title", "My Cheeses");
        return "cheese/index";

        }

    @RequestMapping(value="add", method = RequestMethod.GET)
        public String dissplayAddCheeseForm(Model model) {
        model.addAttribute("title", "Add Cheese");
        return "cheese/add";


        }
        @RequestMapping(value = "add", method = RequestMethod.POST)
        public String processAddCheeseForm(@RequestParam String cheeseName, @RequestParam String cheeseDesc){
        cheeses.put(cheeseName, cheeseDesc);

        //redirect to cheese
        return "redirect:";
        }


}
