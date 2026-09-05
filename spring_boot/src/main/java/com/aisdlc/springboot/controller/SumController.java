package com.aisdlc.springboot.controller;

import com.aisdlc.springboot.dto.SumResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SumController {

  @GetMapping("/sum")
  public SumResponse sum(@RequestParam int a, @RequestParam int b) {
    return new SumResponse(a + b);
  }
}
