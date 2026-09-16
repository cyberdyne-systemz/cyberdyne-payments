package com.cyberdyne.payments;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(TransferController.class)
class TransferControllerTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void acceptsPositiveAmount() throws Exception {
        mvc.perform(post("/transfer").contentType(MediaType.APPLICATION_JSON).content(request("12.50")))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").isNotEmpty())
                .andExpect(jsonPath("$.amount").value(12.50))
                .andExpect(jsonPath("$.status").value("accepted"));
    }

    @Test
    void rejectsMissingAmount() throws Exception {
        mvc.perform(post("/transfer").contentType(MediaType.APPLICATION_JSON).content(request("null")))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"))
                .andExpect(jsonPath("$.errors[0].field").value("amount"))
                .andExpect(jsonPath("$.errors[0].message").value("amount is required"));
    }

    @Test
    void rejectsUnsupportedCurrency() throws Exception {
        mvc.perform(post("/transfer").contentType(MediaType.APPLICATION_JSON)
                        .content(request("12.50").replace("USD", "GBP")))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errors[0].message").value("currency must be USD or EUR"));
    }

    @Test
    void rejectsMalformedJson() throws Exception {
        mvc.perform(post("/transfer").contentType(MediaType.APPLICATION_JSON).content("{"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("INVALID_JSON"));
    }

    @Test
    void rejectsNegativeAmountWithClearFieldError() throws Exception {
        mvc.perform(post("/transfer").contentType(MediaType.APPLICATION_JSON).content(request("-1.25")))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"))
                .andExpect(jsonPath("$.errors[0].field").value("amount"))
                .andExpect(jsonPath("$.errors[0].message").value("amount must be greater than or equal to 0"));
    }

    @Test
    void rejectsSmallNegativeDecimal() throws Exception {
        mvc.perform(post("/transfer").contentType(MediaType.APPLICATION_JSON).content(request("-0.01")))
                .andExpect(status().isBadRequest());
    }

    @Test
    void acceptsZeroAmount() throws Exception {
        mvc.perform(post("/transfer").contentType(MediaType.APPLICATION_JSON).content(request("0")))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.amount").value(0));
    }

    private String request(String amount) {
        return """
                {"sourceAccount":"acct-100","destinationAccount":"acct-200","amount":%s,"currency":"USD"}
                """.formatted(amount);
    }
}
