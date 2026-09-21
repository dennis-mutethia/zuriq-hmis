# Zuriq 1.0 — Inferred Database Schema (from decompiled source)
Extracted automatically from embedded SQL in TableAdapter classes. This is best-effort (built from SELECT/INSERT statements actually used in the app), not a full DDL dump — some rarely-touched columns may be missing, and data types are not shown (only in the .xsd DataSet designer files, not yet parsed here).

## tblaccounts
AccountID, AccountNo, AccountTypeID, Name

## tblaccounttypes
AccountTypeID, Name

## tblaccsubacc
AccSubAccID, AccountID, SubAccountID

## tbladmissiondoctornotes
AdmissionID, Notes, SystemUserId, dateTimePosted

## tbladmissionform
AdmissionID, Allergies, BloodPressure, DateTimePosted, Diagnosis, GeneralCondition, HPI, Investigations, PastMedicalHistory, Pulse, RespirationRate, ReviewOfSystems, SocialHabits, Temperature, Treatment

## tbladmissionnotes
AdmissionID, DateTimePosted, Notes, SystemUserID

## tbladmissionprescriptionitems
DateTimeSold, MedicalBillID, Name, Quantity, SystemUserID

## tbladmissions
AdmissionDateTime, AdmissionID, AdmittedBySysUserID, AdmittingDoctor, DischargeDateTime, DischargingDoctor, IsInAdmission, PatientID, ReceivedByNurse, VisitID

## tbladmissionward
AdmissionID, BedID, IsCurrentBed, WardID

## tblarinvoicecashpayments
ARInvoiceID, AmountPaid, DateTimePaid, IssuedReceiptID, PaidInBy

## tblarinvoicechequepayments
ARInvoiceID, Amount, AmountInWords, Branch, ChequeIsProcessed, ChequeIssueDate, ChequeNo, DateTimeReceived, Drawee, DraweeAccountNo, Drawer, DrawerAccountNo, DrawerBank, IssuedReceiptID, IssuingBank, ReceivedFrom, ReferenceNo

## tblarinvoicecorporatedetails
ArInvoiceID, CompanyName, DateTimeOfAdmission, DateTimeOfDischarge, DoctorName, InPatientNo, MembershipNo, OutPatientNo, PrincipalMember, Sponsor, Terms

## tblarinvoicediscounts
ARInvoiceID, DateTimePosted, DiscountAmount, SystemUserID

## tblarinvoicemedicalbill
ARInvoiceID, MedicalBillID

## tblarinvoicerebates
ARInvoiceID, CoverAmount1, CoverAmount2, Description1, Description2, SystemUserID

## tblarinvoices
ARInvoiceID, ARInvoiceNo, Address, AmountReceivable, CancellationReason, CancelledBySysUID, CoverAmount, CreditNoteAmount, CreditNoteReason, DateTimeCreated, DepositAccSubAccID, DueDate, EmailAddress, HasBeenCancelled, HasWriteOff, IDNumber, InvoiceTo, IsPaid, IsProcessed, IsProfoma, Name, OrderNo, PhoneNumber, PreparedBy, ReceivableAccSubAccID, SalesDiscountAmount, Telephone1, Telephone2, TotalAmountPaid, WriteOffAmount, WriteOffBySysUID, WriteOffReason

## tblassetregisters
AssetRegisterID, CostPerUnit, DepartmentID, Model, Name, Status, StorageLocationID, Units

## tblbalances
FromDateTime, NetBalance, SubAccountID, ToDateTime

## tblbankbranch
BankBranchID, BankID, BranchCode, Name

## tblbankdeposits
AmountInWords, BankTransactionRefNo, ChequeNos, DateTimeDeposited, DepositedBy, DestAccSubAccID, JournalVoucherID, TotalAmount

## tblbankrec
BankRecID, BookBalance, FromDateTime, HasBeenReconciled, ReconciledBySysUID, StatementBalance, ToDateTime

## tblbankrecitems
BankRecID, IsAdjustment, IsBankAdjustingItem, IsBookAdjustingItem, IsIncrement, SubAccountEntryID

## tblbanks
BankCode, BankID, Name

## tblbeds
BedID, BedNo, BedStatus, WardID

## tblblacklistpatients
DateTimeBlacklisted, IsBlackListed, PatientID, Reason, SystemUserID

## tblbloodtransfusion
AdmissionID, BloodPressure, Comments, DateTimePosted, Pulse, Respiratory, SystemUserID, Temperature

## tblbor
BOR, BORID, FromDateTime, ToDateTime, WardName

## tblcardex
AdmissionID, DateTimePosted, Notes, SystemUserID

## tblcheques
AmountInWords, ChequeID, ChequeNo, DateTimePayable, JournalVoucherID, PaidTo

## tblclinics
ClinicID, Name

## tblcollectionbatches
BatchID, DateTimePosted, SystemUserID

## tblcollections
Amount, BatchID, DateTimePosted, DepartmentID, IsPosted, Mpesa, SystemUserID

## tblcomplaints
ComplaintID, Description

## tblconsentform
Operation, OperationDate, PatientID, TheatreQueueID, Witness

## tblconsultantbillitems
ConsultantID, DateTimeSold, IsProcessed, ItemName, NetAmount, SaleItemID

## tblconsultantbills
ConsultantBillID, ConsultantID, DateTimeCreated, HospitalDeduction, IsCleared, NetAmount, PreparedBySysUID, TotalAmount, TotalAmountPaid

## tblconsultants
Alias, ConsultantID, Designation, MobileNo1, OtherNames, Surname

## tblconsultantsbookings
ConsultantID, DatetimeBooked, IsSeen, PatientID, VisitDateTime

## tblcontinuationsheet
AdmissionID, Notes, SystemUserId, dateTimePosted

## tblcreditnotes
Address, CreditNoteID, CreditNoteNo, CustomerName, EmailAddress, JournalVoucherID, TelephoneNo, TotalAmount

## tblcustomerdeposits
CustomerName, MedicalBillID, PatientID, TotalAmountDeposited, TotalAmountUsed

## tblcwc
CWCNO, DangerSigns, DateTimeCreated, FollowUpReason, IsIssued, IsRevisit, IsUnderWeight, ReferalReason, VisitID, Weight

## tbldeliverynoteitems
Amount, DeliveryNoteID, ItemName, NetAmount, PerDiscount, PerVAT, Quantity, Rate, UnitOfMeasure, VATTypeID

## tbldeliverynotes
Comment, CustomerName, DateTimeCreated, DateTimeDelivered, DeliveryNoteID, PhysicalAddress, ReceivedBy, TelephoneNo1

## tbldentistresults
Center, Comments, DatePosted, DentalResultsID, Diagnosis, DoctorID, Examinations, Examiner, Findings, Histoy, Impression, IsDental, MedReqOExamID, PatientComplaints, SystemUserID, TreatmentDone, TreatmentPlan, VisitID

## tbldepartments
DepartmentID, Name

## tbldiabetesmonitor
AdmissionID, DateTimePosted, FBS, Intervention, RBS, SystemUserID

## tbldiagnosis
Description, DiagnosisID

## tbldischargesummary
AdmissionID, Admittedduration, Comments, Diagnosis, DischargePrescription, DischargedBySysUserID, ExaminationFindings, HasNextAppointment, History, InvestigationsResults, IsAlive, IsReferal, NextAppointmentDateTime, TreatmentGiven

## tbldischargesummary_1
AdmissionID, Admittedduration

## tbldoctors
DoctorID, Name, Registration

## tbldonationexpenditures
Amount, ApprovedBy, DateTimeUsed, DonationExpenditureID, DonationID, Purpose

## tbldonations
AmountDonated, AmountUsed, DateTimeDonated, DeadlineDateTime, DonationID, DonorID

## tbldonetestscomponents
DateTimeDone, MedReqTestID, Remark, TestComponentID, TestControlID, TestID, Value

## tbldonors
Contact, Donor, DonorID, DonorTypeID, PhysicalLocation

## tbldonortypes
DonorTypeID, DonorTypeName

## tblemployeepayrollparameter
Amount, EmployeeID, PayrollParameterID

## tblemployeepayslipparameter
Amount, EmployeeID, EmployeePayslipParameterID, PayrollParameterID, PayslipPeriodID

## tblemployees
BankAccountNo, BankBranchID, DateEmployed, DepartmentID, Designation, EmployeeID, EmploymentTypeID, IDNo, IDTypeID, NHIFNo, NSSFNo, OtherNames, PINNo, PaymentModeID, PayrollNo, StaffNo, Surname, Telephone1

## tblemploymenttypes
EmploymentTypeID, Name

## tblendofshiftreconciliations
ActualBalance, BalanceDifference, BeginDateTime, EndDateTime, ExpectedClosingBalance, Explanation, NetCashTransactions, OpeningBalance

## tbleod
AirtelMoney, Cash, CashBoxTotals, Cheque, CreditCard, DebitCard, DirectBank, EFT, EODID, Mpesa, Notes, ShiftID, SystemUserID, TotalCollections

## tblexpensepayments
AmountPaid, DateTimePaid, ExpenseID, PaidTo, ReceivedReceiptNo, SystemUserIDPaidOutBy

## tblexpenses
Balance, DateDue, DateTimeIncurred, Description, ExpenseID, Name, TotalAmount, TotalAmountPaid

## tblfamilysocioeconomics
Description, FamilySocioEconomicID

## tblfinancials
AccountReceivable, AccountsPayable, AccruedIncomeTaxes, AccruedLiabilities, AccumulatedDepreciation, Bank, Buildings, Cash, CommonStock, CostOfGoodsSold, CustomerDeposits, DeferredIncomeTaxes, DepreciationExpenses, Equipment, FinancialID, FiscalPeriodID, FixturesAndFittings, FromDateTime, Furniture, IncomeTaxes, InterestExpenses, Inventory, Land, LongTermDebts, MotorVehicle, NetSales, NotesPayable, OpeningBalanceEquity, OtherAssets, OtherCurrentAssets, OtherCurrentLiabilities, OtherIncome, OtherIncomeExpenses, PreferredStock, RetainedEarnings, SellingAdminGeneralExpenses, StatementDate, Taxes, ToDateTime

## tblfiscalperiods
CloseDate, FiscalPeriodID, OpenDate

## tblfluidsmonitor
AdmissionID, DateTimePosted, FluidsMonitorID, IVFluids, NGT, SystemUserID, TotalInput, TotalOutPut, Urine, Vomitus

## tblgatepass
ARInvoiceID, DateTimePosted, OutPatientNo, PatientName

## tblgrnitems
BatchNo, Description, EarliestExpiryDate, GRNID, Name, NetAmount, PerDiscount, PerVAT, ProductID, Quality, QuantityOrdered, QuantityReceived, Rate, UnitOfMeasure, VATInclusiveAmount

## tblgrns
APInvoiceNo, DateTimeCreated, DeliveryNoteNo, GRNID, HasBeenChecked, HasBeenReceived, IsCommittedToStock, PurchaseOrderID

## tblgroupaccounts
CappingDays, CoPayAmount, ContractAmount, CreditLimit, EmailAddress, GroupAccountID, HasCoPay, HasVisitDaysCap, IsActive, Name, PhysicalAddress, PostalAddress, PostalCode, ReceivableAccSubAccID, Telephone1, TownCity

## tblhospitalinfo
HospitalInfoID, LetterHead, Logo, Name

## tblhospitalinfo_1
HospitalInfoID, LetterHead, Logo, Name

## tblidtypes
IDType, IDTypeID

## tblimpressions
Description, ImpressionID

## tblinpatientrequestitems
Code, DateTimeDispensed, DispensedBySysUID, HasBeenDispensed, InpatientRequestID, Name, Quantity

## tblinpatientrequests
DateTimeRequested, IsProcessed, MedicalBillID, StorageLocationID, SystemUserID

## tblinternalorderitems
EarliestExpiryDate, InternalOrderID, InternalOrderItemID, IssuedTotalPackedQuantity, ProductID, QuantityIssued, QuantityOrdered, UnitCost, UnitOfMeasure, UnitPrice

## tblinternalorders
ApprovedBySysUserID, DateTimeDispatched, DateTimeReceived, DateTimeSent, HasBeenApproved, HasBeenSent, InternalOrderID, IsReturnedStock, IssuingLocationComment, IssuingStorageLocationID, ItemsDispatchedBySysUserID, ItemsReceived, ItemsReceivedBySysUserID, OrderItemsDispatched, OrderStatus, RequestingLocationComment, RequestingStorageLocationID

## tblissuedreceipts
ARInvoiceID, AmountPaid, AmountReceived, CancellationReason, CancelledBySysUID, CardNo, ChangeAmount, ChequeDate, ChequeDrawer, ChequeIssuingBank, ChequeIssuingBranch, ChequeNo, DateTimeIssued, Description, HasBeenCancelled, IsCashSale, IsCustomerDeposit, IsDebtorPayment, IsRejected, IsSplitPayment, IssuedReceiptID, IssuedReceiptNo, IssuedTo, MedicalBillID, PaidInBy, PaymentFor, PaymentIsProcessed, PaymentModeID, PaymentRefNo, RejectionReason, SystemUserIDIssuedBy

## tblitemcategory
ItemCategoryID, Name

## tbljournalvouchers
Description, FiscalPeriodID, JournalVoucherID, SourceReference, SystemUserID, TransactionAmount, TransactionDateTime

## tbllabdatasummary
Btn5And14Pos, Btn5And14Tested, FemaleTotal, FromDateTime, GreaterThan14Pos, GreaterThan14Tested, High, LabDataSummaryID, LessThan5Pos, LessThan5Tested, Low, MaleTotal, Normal, Test, TestComponent, ToDateTime, Total, VeryLow

## tbllessthan7daysvisits
DateTimePosted, LastVisitDateTime, PatientID, Reason, SystemUserID

## tbllimitprescriptionqty
MaximumPrescriptionQty, ProductID

## tbllockedbills
DatetimeLocked, IsLocked, MedicalBillID, Name, PledgeDate, SystemUserID, Telephone

## tbllockproduct
GroupAccountID, ProductID

## tbllockservice
GroupAccountID, ServiceID

## tblmaternityadmissionexamination
Abnormalities, AdmissionID, BP, Enlargement, FetalHeart, Genitals, HB, Height, HeightOfFundus, PatientID, Position, Presentation, Spleen, SystemUserID, TPR, Urine, VaginalDischarge, Weight

## tblmaternitybehead
AdmissionID, Clinic, DateTimePosted, Diagnosis, EDD, EducationLevel, Gravida, LMP, Occupation, Para, PatientID, PeriodOfGestation, SystemUserID

## tblmaternityfamilyhistory
AdmissionID, Assessment, DOB, Delivery, DurationOfLabor, Feeding, IsAlive, Place, Puerparium, Sex, SystemUserID, Weight

## tblmedcomp
ComplaintID, VisitID

## tblmeddiagnosis
Diagnosis, VisitID

## tblmeddiagpres
DiagnosisID, VisitID

## tblmedfamsocecon
FamilySocioEconomicID, PatientID, VisitID

## tblmedicalbillpayments
ARInvoiceID, AmountPaid, CardNo, ChequeDate, ChequeDrawer, ChequeIssuingBank, ChequeIssuingBranch, ChequeNo, DateTimePaid, IsCash, IsRejected, IssuedReceiptID, MedicalBillID, PaidInBy, PaymentIsProcessed, PaymentRefNo, RejectionReason, SystemUserIDReceivedBy

## tblmedicalbills
AdvancePayment, CoverAmount, CustomerName, DateTimeCreated, DateTimeProcessed, DepositBalance, DepositOffset, GroupAccountID, IDNumber, IsPatient, IsProcessed, MedicalBillID, MedicalBillNo, OtherNames, ProcessedBySysUserID, SalesDiscountAmount, Surname, TelephoneNo, TotalAmountPaid, TotalBillAmount, VisitID, WriteOffAmount

## tblmedicalinfos
Age, AgeMonths, AgeWeeks, ClinicID, Doctor, HPI, IsAdmitted, Nurse, PatientID, Summary, SystemUserID, VisitDateTime, VisitID

## tblmedicalsurgicalhistories
Description, MedicalSurgicalHistoryID

## tblmedimp
ImpressionID, VisitID

## tblmedinfo
IllnessDuration, IsAlive, IsFollowUp, IsReferal, IsRevisit, ReferalReason, Treatment, VisitID

## tblmedopticalreqtests
Age, AgeMonths, AgeWeeks, MedReqTestID, OtherNames, Sex, Surname, VisitID

## tblmedpres
PrescriptionID, VisitID

## tblmedreqdentalexam
Age, DateTimeRequested, MedReqOExamID, OtherNames, OutPatientNo, Sex, Surname, TelephoneNo, VisitID

## tblmedreqdentalexamitemsii
Center, Comment, DateTimeDone, Examiner, Findings, History, Impression, IsDone, IsInternal, MedReqOExamID, ReasonNotDone, RequestedBySysUID, ServiceID, TechniqueProcedure

## tblmedreqoexam
Age, DateTimeRequested, EmailAddress, MedReqOExamID, OtherNames, OutPatientNo, PostalAddress, PostalCode, Sex, Surname, TelephoneNo, VisitID

## tblmedreqoexamitems
Center, Comment, DateTimeDone, Examiner, Findings, History, Impression, IsDone, IsInternal, MedReqOExamID, OExaminationID, ReasonNotDone, RequestedBySysUID, TechniqueProcedure

## tblmedreqopticalexam
Age, DateTimeRequested, IsOutPatient, IsSelfRequest, MedReqOExamID, OtherNames, OutPatientNo, Sex, Surname, TelephoneNo, VisitID

## tblmedreqopticalexamitems
Center, Comment, DateTimeDone, Examiner, Findings, History, Impression, IsDone, IsInternal, MedReqOExamID, MedReqOExamItemID, OExaminationID, ReasonNotDone, RequestedBySysUID, TechniqueProcedure

## tblmedreqtestitems
Conclusion, MedReqTestID, MedReqTestItemID, Test, TestID

## tblmedreqtests
Age, AgeMonths, AgeWeeks, DateTimeDone, DateTimeRequested, IsDone, IsInternal, IsOutPatient, IsSelfRequest, MedReqTestID, OtherNames, OutPatientNo, ReasonNotDone, RequestedByID, Sex, Surname, Technologist, VisitID

## tblmedsexam
SExaminationID, SRemarkID, VisitID

## tblmedsurghis
MedicalSurgicalHistoryID, PatientID, VisitID

## tblnationality
Name, NationalityID

## tblnursecareplan
AdmissionID, Assessment, DateTimePosted, Evaluation, ExpectedOutcome, Implementation, NursingDiagnosis, NursingInterventions, ScientificRationale, SystemUserID

## tblnursetriage
BloodPressure, BloodPressureRemarks, Notes, NurseTriageID, PulseRate, PulseRateRemarks, RespirationRate, RespirationRateRemarks, Temperature, TemperatureRemarks, VisitID, Weight, WeightRemarks

## tblobservationchart
AdmissionID, Comments, DateTimePosted, Diastolic, Pulse, Respiratory, SPo2, SystemUserID, Systolic, Temperature

## tbloexaminations
Description, OExaminationID

## tblopticalnotes
Complaints, DatePosted, Diagnosis, DoctorID, Examinations, Histoy, MedReqTestID, OpticalNotesID, Treatment, TreatmentDone, TreatmentPlan, VisitID

## tblopticaltexaminations
Description, OExaminationID

## tblorthopedic
DateTimePosted, Diagnosis, Management, Notes, OrthopedicID, SystemUserID, VisitID

## tblpatients
CityTown, CompanyName, DateOfBirth, DateRegistered, EmailAddress, GroupAccountID, IDNumber, IDTypeID, InPatientNo, MembershipNo, NationalityID, NextOfKin, NextOfKinContact, NextOfKinRelationship, Note, Occupation, OtherNames, OutPatientNo, PatientID, PostalAddress, PostalCode, PrincipalMember, ReferenceNo, RegisteredBySysUID, Residence, Sex, Surname, Telephone1, Telephone2, ThirdName

## tblpatienttemperatures
InPatientNo, OutPatientNO, TempDateTimeDone, Value

## tblpaymentmodecategories
Name, PaymentModeCategoryID

## tblpaymentmodes
Name, PaymentModeCategoryID, PaymentModeID

## tblpayrollparametercategories
Name, ParameterCategoryType, PayrollParameterCategoryID

## tblpayrollparameters
Name, PayrollParameterCategoryID, PayrollParameterID

## tblpayslipperiods
BeginningDateTime, EndingDateTime, PayMonth, PayYear, PayslipPeriodID

## tblpayslips
BasicPayTotal, CommuterAllowanceTotal, DeductionTotal, ElectricityAllowanceTotal, EmployeeID, EmployerContributionTotal, FringeBenefitTaxTotal, GrossEarningTotal, GrossTaxablePayTotal, HousingAllowanceTotal, IsPaid, LeaveAllowanceTotal, LoanRepaymentTotal, NHIFTotal, NSSFReliefTotal, NSSFTotal, NetPay, OtherAllowanceTotal, OtherDeductionTotal, OtherPensionReliefTotal, OtherPensionTotal, OverTaxationTotal, OvertimeTotal, PAYETotal, PayslipID, PayslipPeriodID, PersonalReliefTotal, SaccoTotal, SalaryAdvanceRecoveryTotal, TaxChargeableTotal, TaxableAmountTotal, UnderPaymentTotal

## tblphysioresults
Complaints, DatePosted, Diagnosis, Examinations, IsOptical, IsOrthopaedic, IsPhysio, SystemUserID, Treatment, VisitID

## tblprescriptionitems
DosageDuration, DosageUnits, FrequencyPerDay, Inscription, OtherInstruction, PeriodIn, PrescriptionID, PrescriptionItemID, Quantity, QuantityPerTime, Subscription, Transcription

## tblprescriptions
Description, PrescriptionID, PrescriptionNo, SpecialInstruction

## tblproducts
AAR, Code, Description, EduAfya, Jubilee, KCB, Liason, MaklG4SPamoja, MaklKWFTAfyaFit, MaklServiceProvider, MaklTSC2021, MinetFamilyBank, MinetNSSF, MinetSafaricom, Mtiba, NHIFFFS, NHIFNPS, Name, NationalScheme, ProductID, Quality, Resolution, SahamMua, UnitCost, UnitDefination, UnitPrice

## tblproductstoragelocation
EarliestExpiryDate, ProductID, Quantity, ReorderLevel, StorageLocationID

## tblpurchaseorderitems
Amount, Description, DiscountedAmount, Name, PercentageDiscount, PercentageVAT, PurchaseOrderID, Quality, Quantity, Rate, UnitDefination

## tblpurchaseorders
CheckedByID, CommittedToStock, DateTimeChecked, DateTimeIssued, DateTimeReceived, DeliveryNoteNo, HasBeenChecked, HasBeenReceived, InvoiceNo, OrderNo, OrderReference, PreparedByID, PurchaseOrderID, PurchaseOrderNo, ReceivedByID, SupplierID, TermsConditions, Validitydate

## tblreceiptsrefunds
DateTimePosted, IssuedReceiptID, Reason, RefundAmount, SystemUserID

## tblreferalform
ClinicalNotes, DateTimeReferred, Diagnosis, Investigations, PatientID, ReferedBy, ReferedReason, ToDoctor, ToHospital, Treatments, referalformID

## tblsaleitems
ARInvoiceID, Amount, Code, CostAmount, DateTimeSold, DepartmentID, Description, DiscountedAmount, DispensedBySysUID, HasBeenDispensed, HasBeenPaidFor, IsCashSale, IsConsumable, IssuedReceiptID, ItemCategoryID, MedicalBillID, Name, PercentageDiscount, Quantity, Rate, SaleItemID, StorageLocationID, SubAccountID, SystemUserID, VAT, VATAmount

## tblsalesorderitems
Amount, Code, DepartmentID, ItemCategoryID, ItemName, NetAmount, PercentageDiscount, PercentageVAT, QuantityOrdered, Rate, SalesOrderID, SalesOrderItemID, StorageLocationID

## tblsalesorders
CreatedBySysUID, CustomerName, DateTimeCreated, IsProcessed, SalesOrderID

## tblserviceproduct
ProductID, ServiceID

## tblserviceproductcost
Cost, MedicalBillID, ProductID, RequiredQuantity, RequiredQuantityUnits, ServiceID

## tblservices
AAR, CashRate, DepartmentID, EduAfya, KCB, Liason, NHIFFFS, Name, NationalScheme, ServiceID

## tblsexaminationremarks
Remark, SExaminationID, SRemarkID

## tblsexaminations
Description, SExaminationID

## tblshiftarinvoices
ARInvoiceID, DateTimePosted, ShiftID

## tblshiftmanager
BeginDateTime, ClosedBySystemUserID, EndDateTime, IsOpen, ShiftID, SystemUserID

## tblshifts
BeginDateTime, EndDateTime, IsOpen, ShiftID, SystemUserID

## tblsicksheet
DateTimePosted, Duration, EndDateTime, PatientID, Reason, Recomendation, SickSheetID, StartDate, SystemUserID, VisitID

## tblspecimen
Name, SpecimenID

## tblsplitcheque
BankName, ChequeID, ChequeNo

## tblsplitchequeitems
Amount, AmountInWords, ChequeID, DateTimePayable, PaidTo, SplitChequeitemID

## tblstockchange
ChangeTypeID, DateTimeChanged, IsIncrement, ProductID, QuantityChanged, Reference, StorageLocationID, SystemUserID

## tblstoragelocations
Name, StorageLocationID

## tblstoragelocations_1
Name, StorageLocationID

## tblsubaccountentries
AccSubAccID, AccountType, Amount, EntryType, FiscalPeriodID, JournalVoucherID, SubAccountEntryID, TransactionDateTime

## tblsubaccounts
Name, SubAccountID

## tblsupplierbillitems
Amount, Item, NetAmount, PercentageDiscount, PercentageVAT, Quantity, SupplierBillID, UnitCost, UnitOfMeasure

## tblsupplierbillpayments
AmountPaid, ChequeNo, JournalVoucherID, PaymentModeID, PettyCashVoucherNo, ReceiptNo, ReferenceNo, SupplierBillID

## tblsupplierbills
APInvoiceNo, DateTimeApproved, DateTimeCreated, DateTimeDue, IsApproved, IsSettled, JournalVoucherID, PurchaseOrderID, ReferenceNo, SupplierBillID, SupplierBillNo, SupplierID, SystemUserID, Terms, TotalAmountPaid, TotalCreditNoteAmount, TotalNetAmount

## tblsuppliercreditnoteitems
CreditReason, Item, NewAmount, NewNetAmount, NewPercentageDiscount, NewPercentageVAT, NewQuantity, NewUnitCost, NewUnitOfMeasure, SupplierCreditNoteID

## tblsuppliercreditnotes
SupplierBillID, SupplierCreditNoteID, SupplierCreditNoteNo

## tblsuppliers
ContactPerson, Country, Description, EmailAddress, Name, PhysicalAddress, PostalAddress, PostalCode, SupplierID, Telephone1, Telephone2, TownCity, WebAddress

## tblsystemusers
SystemUserID, Username

## tbltbscreening
IsCough, IsFever, IsLossWeight, IsNightSweats, IsPositive, IsReducedPlay, IsUnder5, TBScreeningID, VisitID

## tbltempcollections
Amount, DepartmentID, IsPosted, Mpesa

## tbltempqueue
DateTimeCreated, FromRoom, OtherNames, OutPatientNo, QueueDateTimeIn, QueueDateTimeOut, QueueID, QueueItemID, RoomDateTimeIn, RoomDateTimeOut, ServiceTime, Surname, ToRoom, TotalTime, WaitingTime

## tbltestcomponents
Name, NormalRange, TestComponentID, Units

## tbltestcontrols
Name, TestControlID

## tbltests
Name, SpecimenID, TestID

## tbltheatre
AdmissionID, DateTimePosted, IsDone, Operation

## tbltheatrechecklistdoctor
AdmissionID, Anaesthetist, BP, BloodAvailable, BloodType, CertifiedBy, Datetimeposted, ElectrocytesNormal, HB, HasConsentGiven, IsChestNormal, IsFitForOperation, IsPremed, IsUrinalysisNormal, Litres, MedicalHistory, Operation, PCV, PremedAmount, PremedTime, PremedType, Pulse, SystemUserID, Temp

## tbltheatrechecklistnurse
AdmissionID, Albumin, BP, CertifiedBy, DateTimePosted, Dentures, FetalHeart, GastricTime, GastricType, Hb, IDTag, InfusionAmount, InfusionType, IsAppropriateGown, IsBladderEmpty, IsBowelEmpty, IsCatheterization, IsEnema, IsGastricLubeGiven, IsInfusionGiven, IsMedicationGiven24hrs, IsPremedication, IsShaving, IsUreaTested, IsXrayTaken, IsXrayWithPatient, Jewellery, MedTime, MedType, Operation, PremedTime, PremedType, Prostheres, Pulse, Starved, Sugar, SystemUserID, TheatreChecklistNurseID, Wigs

## tblthreatrechecklistanaesthetist
AdmissionID, Albumin, Allergies, BP, BloodAvailable, BloodType, CertifiedBy, Datetimeposted, Dentures, HB, HasConsentGiven, IsFitForOperation, IsPremed, Litres, MedicalHistory, Operation, PCV, PremedAmount, PremedTime, PremedType, Pulse, Sugar, SystemUserID, Temp, Weight

## tblvirtualinvoices
ARInvoiceID, DateTimePosted, InvoiceAddress, InvoiceName, MemberNo, OPDNo, SystemUserID, TotalAmount, VirtualInvoiceID

## tblvisitsregister
IsReVisit, PatientID

## tblvitals
AdmissionID, Comment, DateTimePosted, SystemUserID, Value, VitalType

## tblwards
Name, WardID
