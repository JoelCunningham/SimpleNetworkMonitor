import { EditOwnerForm } from '#components/forms';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('EditOwnerForm', () => {
  let component: EditOwnerForm;
  let fixture: ComponentFixture<EditOwnerForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditOwnerForm],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(EditOwnerForm);
    component = fixture.componentInstance;
    component.owner = { id: 1, name: 'Test Owner', devices: [] };
    component.ngOnChanges();
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
