package com.aisdlc.springboot;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.aisdlc.springboot.controller.SumController;
import com.aisdlc.springboot.exception.GlobalExceptionHandler;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(SumController.class)
@org.springframework.context.annotation.Import(GlobalExceptionHandler.class)
class SumControllerTest {

  @Autowired private MockMvc mockMvc;

  @Test
  void sumReturnsResultForValidParams() throws Exception {
    mockMvc
        .perform(get("/sum").param("a", "3").param("b", "4"))
        .andExpect(status().isOk())
        .andExpect(content().json("{\"result\": 7}"));
  }

  @Test
  void sumReturns400ForMissingParam() throws Exception {
    mockMvc
        .perform(get("/sum").param("a", "3"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.error").exists());
  }

  @Test
  void sumReturns400ForNonNumericParam() throws Exception {
    mockMvc
        .perform(get("/sum").param("a", "x").param("b", "4"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.error").exists());
  }
}
