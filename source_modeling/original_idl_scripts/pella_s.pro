FUNCTION pella_s, Z, line_select, target_name
;

if(n_elements(target_name) EQ 0) then target_name = ' '

    CuK_fact = 0.27

CASE line_select OF

'Ka': BEGIN
  ap = 3220000.
  bp = 97600.
  dp = -0.39
; Special for Beryllium
; 6/14/94  Use 5kV  C data for this tweak, as a guess
  if (Z EQ 4) then begin
    ap = 30. * ap
    dp = 30. * dp
  end
; Special for Boron
; Copy Carbon values...
  if (Z EQ 5) then begin
    ap = 30. * ap
    dp = 30. * dp
  end
; Special for Carbon
; 6/14/94  Use 5kV  C data for this tweak
  if (Z EQ 6) then begin
    ap = 30. * ap
    dp = 30. * dp
  end
; Special for MgO
; 6/14/94  Use 5kV MgO data for this tweak
  if (Z EQ 12 OR target_name EQ 'MgO') then begin
    ap = 2.4 * ap
    dp = 2.4 * dp
  end
; Special for Aluminum
; 6/14/94  Use 5kV  Al data for this tweak
  if (Z EQ 13) then begin
    ap = 3.0 * ap
    dp = 3.0 * dp
  end
; For Si use Special for Aluminum
; 6/14/94  Use 5kV  Al data for this tweak
  if (Z EQ 14) then begin
    ap = 3.0 * ap
    dp = 3.0 * dp
  end
; Special for Ti
; 12/21/94  Use 9kV  Ti data for this tweak
  if (Z EQ 22) then begin
    ap = 1.05 * ap
    dp = 1.05 * dp
  end
; Special for Nickel - use Cu values
  if (Z EQ 28) then begin
    ap = 0.27 * ap
    dp = 0.27 * dp
  end
; Special for Copper
; 7/1/94  Use 9.8kV  Cu data for this tweak
  if (Z EQ 29) then begin
    ap = CuK_fact * ap
    dp = CuK_fact * dp
  end
END

'Kb': BEGIN
  ap = 513000.
  bp = 205000.
  dp = -0.014
; Special for MgO
; 6/14/94  Use 5kV MgO data for this tweak
  if (Z EQ 12 OR target_name EQ 'MgO') then begin
    ap = 2.4 * ap
    dp = 2.4 * dp
  end
; Special for Aluminum
; 6/14/94  Use 5kV  Al data for this tweak
  if (Z EQ 13) then begin
    ap = 3.0 * ap
    dp = 3.0 * dp
  end
; Special for Ti
; 12/21/94  Use 9kV  Ti data for this tweak
  if (Z EQ 22) then begin
    ap = 1.33 * ap
    dp = 1.33 * dp
  end
; Special for Copper
; 7/1/94  Use 9.8kV  Cu data for this tweak
  if (Z EQ 29) then begin
    ap = CuK_fact * ap
    dp = CuK_fact * dp
  end
END

'La': BEGIN
  ap = 20200000.
  bp = 2650000.
  dp = 0.21
; Special for MgO - giant kludge to do a compound!
; 6/14/94  Use 5kV MgO data for this tweak
  if (target_name EQ 'MgO') then begin
    ap = 12. * ap
    dp = 12. * dp
  end
; Special for AlO - giant kludge to do a compound!
; Upper limit to O line strength due to smd Al.941028.pha data
  if (target_name EQ 'AlO') then begin
    ap = 0.5 * ap
    dp = 0.5 * dp
  end
; Special for SiO - giant kludge to do a compound!
  if (target_name EQ 'SiO') then begin
    ap = 50. * ap
    dp = 50. * dp
  end
; Special for Ti
; 6/16/94  Use 5kV Ti data for this tweak
  if (Z EQ 22) then begin
    ap = 3.6 * ap
    dp = 3.6 * dp
  end
; Special for Cr
; 6/16/94  Use 5kV Cr data for this tweak
  if (Z EQ 24) then begin
    ap = 4.5 * ap
    dp = 4.5 * dp
  end
; Special for Fe
; 6/5/95  Use 10kV Fe data for this tweak
  if (Z EQ 26) then begin
    ap = 4.25 * ap
    dp = 4.25 * dp
  end
; Special for Cu
; 6/16/94  Use 5kV Cu data for this tweak
  if (Z EQ 29) then begin
    ap = 4. * ap
    dp = 4. * dp
  end
; Special for Nb
;  copied from Mo
  if (Z EQ 41) then begin
    ap = 0.6*3.3 * ap
    dp = 0.6*3.3 * dp
  end
; Special for Mo
; 6/16/94  Use 5kV Mo data for this tweak
; 12/21/94 Use 9kV Mo data for this tweak
  if (Z EQ 42) then begin
    ap = 0.6*3.3 * ap
    dp = 0.6*3.3 * dp
  end
; Special for Ag
;  copied from Mo
  if (Z EQ 47) then begin
    ap = 0.6*3.3 * ap
    dp = 0.6*3.3 * dp
  end
; Special for Sn
;  copied from Mo
  if (Z EQ 50) then begin
    ap = 0.6*3.3 * ap
    dp = 0.6*3.3 * dp
  end
END

'Lb': BEGIN
  ap = 17600000.
  bp = 6050000.
  dp = -0.09
; Special for Ti
; 6/16/94  Use 5kV Ti data for this tweak
  if (Z EQ 22) then begin
    ap = 3.6 * ap
    dp = 3.6 * dp
  end
; Special for Cr
; 6/16/94  Use 5kV Cr data for this tweak
  if (Z EQ 24) then begin
    ap = 4.5 * ap
    dp = 4.5 * dp
  end
; Special for Cu
; 6/16/94  Use 5kV Cu data for this tweak
  if (Z EQ 29) then begin
    ap = 4. * ap
    dp = 4. * dp
  end
; Special for Nb
;   copied from Mo
  if (Z EQ 41) then begin
    ap = 0.6*3.3 * ap
    dp = 0.6*3.3 * dp
  end
; Special for Mo
; 6/16/94  Use 5kV Mo data for this tweak
; 12/19/94 data too
  if (Z EQ 42) then begin
    ap = 0.6*3.3 * ap
    dp = 0.6*3.3 * dp
  end
; Special for Ag
;   copied from Mo
  if (Z EQ 47) then begin
    ap = 0.6*3.3 * ap
    dp = 0.6*3.3 * dp
  end
; Special for Sn
;   copied from Mo
  if (Z EQ 50) then begin
    ap = 0.6*3.3 * ap
    dp = 0.6*3.3 * dp
  end
END

'Ma': BEGIN
  ap = 20200000.
  bp = 2650000.
  dp = 0.21
    if(Z EQ 42) then begin
      ap = 18. * ap
      dp = 18. * dp
    end
    if(Z EQ 74) then begin
      ap = 8. * ap
      dp = 8. * dp
    end
END

'Mb': BEGIN
  ap = 17600000.
  bp = 6050000.
  dp = -0.09
    if(Z EQ 42) then begin
      ap = 18. * ap
      dp = 18. * dp
    end
    if(Z EQ 74) then begin
      ap = 8. * ap
      dp = 8. * dp
    end
END

ELSE: BEGIN
  print, ' labx_linetoc: no information on line type = ',line_select
  return, 0.
  END

ENDCASE

fp = (ap/(bp+Z^4)+dp)

RETURN, fp
END
