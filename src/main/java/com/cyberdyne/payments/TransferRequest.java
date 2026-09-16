package com.cyberdyne.payments;

import java.math.BigDecimal;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public record TransferRequest(
        @NotBlank(message = "sourceAccount is required") String sourceAccount,
        @NotBlank(message = "destinationAccount is required") String destinationAccount,
        @NotNull(message = "amount is required")
        @DecimalMin(value = "0", inclusive = false, message = "amount must be greater than 0") BigDecimal amount,
        @NotBlank(message = "currency is required")
        @Pattern(regexp = "USD|EUR", message = "currency must be USD or EUR") String currency) {
}
