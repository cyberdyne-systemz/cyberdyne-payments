package com.cyberdyne.payments;

import java.math.BigDecimal;
import java.util.UUID;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TransferController {
    @PostMapping("/transfer")
    @ResponseStatus(HttpStatus.CREATED)
    public TransferReceipt transfer(@Valid @RequestBody TransferRequest request) {
        return new TransferReceipt(UUID.randomUUID().toString(), request.amount(), request.currency(), "accepted");
    }

    public record TransferReceipt(String id, BigDecimal amount, String currency, String status) {
    }
}
