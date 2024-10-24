subroutine compute_parameter_sensitivity(parameters, objective, nsamples, nparam, sensitivity)
    implicit none
	real, dimension(nsamples, nparam), intent(in) :: parameters
	real, dimension(nsamples, 1), intent(in) :: objective
	integer, intent(in) :: nsamples, nparam
	real, dimension(nparam),intent(out) :: sensitivity
	integer :: i, j
    real, dimension(nparam) :: mean_param, mean_objective
    real, dimension(nparam) :: covariance, variance_objective
    real, dimension(nparam) :: sensitivity
    integer :: i, j

    ! Initialize parameters and objective with example data
    call initialize_data(parameters, objective, nsamples, nparam)

    ! Compute mean of objective
    mean_objective = sum(objective) / nsamples

    ! Compute covariance and variance for each parameter
    do j = 1, nparam
        ! Compute mean of parameter j
        mean_param(j) = sum(parameters(:, j)) / nsamples

        ! Initialize covariance for parameter j
        covariance(j) = 0.0

        ! Compute covariance between parameter j and the objective
        do i = 1, nsamples
            covariance(j) = covariance(j) + (parameters(i, j) - mean_param(j)) * (objective(i, 1) - mean_objective)
        end do
        covariance(j) = covariance(j) / (nsamples - 1)
        
        ! Compute variance of objective
        variance_objective = sum((objective(:, 1) - mean_objective)**2) / (nsamples - 1)
        
        ! Compute sensitivity for parameter j
        sensitivity(j) = covariance(j) / variance_objective

    end do
	
	! reverse balance to sensitivity
	small_number = 1.0e-6 
	small_bumber = 0.001*minval(sensitivity)
	sensitivity(j) = 1. / (sensitivity(j) + small_number)

    ! Print the results
    print *, 'Sensitivity of parameters:'
    do j = 1, nparam
        print *, 'Parameter ', j, ': ', sensitivity(j)
    end do
	
	return

end subroutine

    subroutine initialize_data(parameters, objective, nsamples, nparam)
        real, dimension(nsamples, nparam), intent(out) :: parameters
        real, dimension(nsamples, 1), intent(out) :: objective
        integer, intent(in) :: nsamples, nparam
        integer :: i, j

        ! Example initialization with random data
        call random_seed()
        do i = 1, nsamples
            do j = 1, nparam
                parameters(i, j) = rand() * 10.0
            end do
            objective(i, 1) = rand() * 100.0
        end do
    end subroutine initialize_data

end program compute_parameter_sensitivity


program optimize_with_parameter_sensitivity
    implicit none

    integer, parameter :: nsamples = 100  ! Number of samples
    integer, parameter :: nparam = 5      ! Number of parameters
    real, dimension(nsamples, nparam) :: parameters
    real, dimension(nsamples, 1) :: objective
    real, dimension(nparam) :: sensitivity
    real :: weight_kge, weight_sensitivity
    real :: kge_error, balanced_objective

    ! Initialize parameters and objective (replace with actual data)
    call initialize_data(parameters, objective, nsamples, nparam)
    call compute_parameter_sensitivity(parameters, objective, nsamples, nparam, sensitivity)

    weight_kge = 1.0
    weight_sensitivity = 0.5
	!Example: Analyze results with weights of 0.1, 0.5, and 0.9 to
	!see how they affect the balance between model accuracy and parameter sensitivity.	

    ! Example of applying sensitivity to the objective function
    do i = 1, nsamples
        kge_error = objective(i, 1)  ! Assuming objective is negative KGE
        balanced_objective = weight_kge * kge_error
        ! Adjust based on sensitivity
        do j = 1, nparam
            balanced_objective = balanced_objective + weight_sensitivity * sensitivity(j)
        end do
        ! Use balanced_objective in your optimization algorithm
    end do

contains

    ! Include the compute_parameter_sensitivity and initialize_data subroutines here

end program optimize_with_parameter_sensitivity


! A) Separate Regularization and Calibration
!1. perform sensitivy analyses: run 1 parameter at a time
!2. calcula S(i=1..npar) = DQ(i)/DPAR(i)
!3. calulate S1 > S2, et.
!4. pesos baseados w(i) =  1/(S(i)+e)

!B) Set up an optimization problem with multiple objectives, such as minimizing streamflow errors and balancing parameter sensitivity.
!multi_objective = weight_kge * kge_error + weight_sensitivity * parameter_sensitivity! Dynamic parameter sensitivity example
!! Function to compute sensitivity based on current parameters
!parameter_sensitivity = compute_sensitivity(current_parameters)
!! Multi-objective function
!multi_objective = weight_kge * kge_error + weight_sensitivity * parameter_sensitivity

!C) Dynamic sensitivity estimation
! C1) Perturbation
!delta = 1e-5 ! Perturbation size
!sensitivity = (objective_function(param + delta) - objective_function(param - delta)) / (2 * delta)

!C2) Covariance based
