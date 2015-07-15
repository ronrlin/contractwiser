# README

##About this package

This package contains a directory and several python source files.

The train/ directory contains a set of files that each corresponds to one kind 
of common legal provision.  For example, train/train_interest_rate contains the 
text from several variations of provisions in legal agreements that can help 
identify the "Interest Rate" provision.   

##Source Code

###identification.py 

The identification module contains the Agreement and AgreementClassifier classes, 
responsible for classifying or categorizing a WHOLE agreement.  For example, the 
identification module will return a result for what type of agreement is being 
analyzed.

###alignment.py 

The alignment module is responsible for classifying or categorizing the provisions WITHIN
an agreement.  








This is just junk to store for later.

def credit_agreement_struct():
    struct = list()
    struct.append('Principal Amount of Loan')
    struct.append('Maturity Date')
    struct.append('Interest Rate')
    struct.append('Conversion to Equity')
    struct.append('Conversion Rate')
    struct.append('Conversion Share Types')
    struct.append('Dilution')
    struct.append('Change in Control')
    struct.append('Acquisition')
    struct.append('Liquidation')
    struct.append('Merger')
    struct.append('Sale of Assets')
    struct.append('IPO')
    struct.append('Events of Default')
    struct.append('Events of Termination')
    struct.append('Prepayment or Make Whole')
    struct.append('Default Interest Rate')
    struct.append('Rights and Remedies for Default')
    struct.append('Payment of Principal')
    struct.append('Payment of Accrued Interest')
    struct.append('Grace Period')
    struct.append('Threshold for Enforcement')
    struct.append('Representations and Warranties of the Company')
    struct.append('Organization')
    struct.append('Good Standing')
    struct.append('No Default')
    struct.append('Charter and Loan Documents')
    struct.append('Organizational Documents')
    struct.append('Corporate Authorization')
    struct.append('Enforceability')
    struct.append('Disclosure of Indebtedness')
    struct.append('Representations and Warranties of the Buyer')
    struct.append('Security Laws Compliance')
    struct.append('Sophistication and Investment Experience')
    struct.append('Qualified Institutional Buyer')
    struct.append('Accredited Investor')
    struct.append('Financial Wherewithal')
    struct.append('Authorization')
    struct.append('Purchase for Own Account')
    struct.append('Information Rights')
    struct.append('Notices and Notification')
    struct.append('Governing Law and Jurisdiction')
    struct.append('Restricted Securities')
    struct.append('Registration')
    struct.append('Assignment and Successor Rights')
    struct.append('Amendment or Modification Rights')
    struct.append('Collection Costs')
    struct.append('Subsequent Sale of Notes')
    struct.append('Use of Proceeds')
    struct.append('Severability')
    struct.append('Waiver of Jury Trial')
    struct.append('Arbitration')
    return struct

