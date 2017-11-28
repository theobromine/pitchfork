use `WebSys`

CREATE TABLE IF NOT EXISTS `pitchfork_payments` (
  PaymentId int NOT NULL auto_increment,
  GroupId int NOT NULL,
  UserId int NOT NULL,
  Amount decimal(5,2) NOT NULL,
  Paid bit NOT NULL,
  PaypalId varchar(50) NULL,
  PaidDate datetime NULL,
  PRIMARY KEY (PaymentId)
);

CREATE TABLE IF NOT EXISTS `pitchfork_payouts` (
  PayoutId int NOT NULL auto_increment,
  GroupId int NOT NULL,
  UserId int NOT NULL,
  Amount decimal(5,2) NOT NULL,
  Paid bit NOT NULL,
  PaypalId varchar(50) NULL,
  PaidDate datetime NULL,
  PRIMARY KEY PayoutId 
);