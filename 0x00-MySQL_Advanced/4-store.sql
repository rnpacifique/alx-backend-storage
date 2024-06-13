-- Create trigger to decrease quantity of an item after adding a new order

-- DROP TRIGGER IF EXISTS trigger_update_quantity;
DELIMITER //
CREATE TRIGGER trigger_update_quantity AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
//
DELIMITER ;