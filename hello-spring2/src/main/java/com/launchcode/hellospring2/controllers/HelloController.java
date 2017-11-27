package com.launchcode.hellospring2.controllers;

import org.apache.catalina.servlet4preview.http.HttpServletRequest;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller

public class HelloController {
    @RequestMapping(value="")
    @ResponseBody
    public String index(HttpServletRequest request){
        String name = request.getParameter("name");
        if (name == null){
            name = "World";
        }

        return "Hello " + name;
    }

    @RequestMapping(value = "hello", method = RequestMethod.GET)
    @ResponseBody

    public String helloForm(){
        String html = "<form method='post'>" +
                "<input type='text' name='name' />" +
                "<select name='lang'>" +
                "  <option value='english'>English</option>" +
                "  <option value='french'>French</option>" +
                "  <option value='spanish'>Spanish</option>" +
                "  <option value='portuguese'>Portuguese</option>" +
                " <option value='cowboy'>Cowboy</option>" +
                "</select>"+

                "<input type='submit' value='Greet Me!'/>" +
                "</form>";
        return html;
    }

    @RequestMapping(value="hello", method= RequestMethod.POST)
    @ResponseBody
    public String createMessage(HttpServletRequest request){
        String name = request.getParameter("name");
        String lang = request.getParameter("lang");
        if (lang.equals("english")){
            return "Hello " + name;}
        if (lang.equals("french")){
            return "Bonjour" + name;}
        if (lang.equals("spanish")){
            return "Hola " + name;}
        if (lang.equals("portuguese")){
            return "Oi " + name;}
        if (lang.equals("cowboy")){
            return "Howdy " + name;}
        else{return "no lang " + name;}
    }

    @RequestMapping(value = "hello/{name}")
    @ResponseBody
    public String helloUrlSegment(@PathVariable String name){
        return "Hello " + name;
    }

    @RequestMapping(value="goodbye")
    public String goodbye(){
        return "redirect:/";
    }

}

