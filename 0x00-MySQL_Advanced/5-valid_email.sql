-- Create trigger to reset valid_email attribute only when email is changed

-- DROP TRIGGER IF EXISTS trigger_reset_valid_email;
DELIMITER //
CREATE TRIGGER trigger_reset_valid_email BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
//
DELIMITER ;